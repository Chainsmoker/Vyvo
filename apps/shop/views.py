import stripe
from django.views.generic import TemplateView, ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from decouple import config
from django.conf import settings
from .models import Product, Category, ProductImage, Review, Order
from .forms import CreateProductForm, ReviewForm
import json

stripe.api_key = config('STRIPE_KEY')

class ShopView(ListView):
    template_name = "shop.html"
    model = Product
    context_object_name = "products"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('-created_at')[:12]
        context['rating'] = {
            'all': Product.objects.all().count(),
            'one_star': Product.objects.filter(reviews__rating=1).count(),
            'two_star': Product.objects.filter(reviews__rating=2).count(),
            'three_star': Product.objects.filter(reviews__rating=3).count(),
            'four_star': Product.objects.filter(reviews__rating=4).count(),
            'five_star': Product.objects.filter(reviews__rating=5).count(),
        }
        search = self.request.GET.get('search')
        if search:
            context['products'] = Product.objects.filter(name__icontains=search).order_by('-created_at')
        
        category = self.request.GET.get('category')
        if category:
            context['products'] = Product.objects.filter(category__name=category).order_by('-created_at')
        rating = self.request.GET.get('rating')
        if rating:
            if rating == 'all':
                context['products'] = Product.objects.all().order_by('-created_at')
            else:
                context['products'] = Product.objects.filter(reviews__rating=rating).order_by('-created_at')
        return context

class ProductView(DetailView):
    template_name = "product-details.html"
    model = Product
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['more_products'] = Product.objects.all().order_by('-created_at')[:9]
        return context

class CartView(TemplateView):
    template_name = "cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', [])
        context['products'] = Product.objects.filter(id__in=cart)
        return context

class CartSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "cart-success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', [])
        context['products'] = Product.objects.filter(id__in=cart)
        return context

@csrf_exempt
def create_product(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            product = form.save(commit=False)
            product.creator = request.user
            product.slug = slugify(product.name)
            product.save()
            
            images = request.FILES.getlist('images')
            for image in images:
                ProductImage.objects.create(product=product, image=image)
            
            return JsonResponse({'success': True, 'url': '/product/' + product.slug})
        else:
            sanitized_errors = {
                field: error[0] for field, error in form.errors.items()
            }
            print(sanitized_errors)
            return JsonResponse({'success': False, 'errors': sanitized_errors})

@login_required
@csrf_exempt
def create_review(request, slug):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product = Product.objects.get(slug=slug)
            user = request.user
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = user
                review.product = product
                review.save()
                return JsonResponse({'success': True})
            else:
                sanitized_errors = {
                    field: error[0] for field, error in form.errors.items()
                }
                return JsonResponse({'success': False, 'errors': sanitized_errors})
        else:
            return JsonResponse({'success': False})

def get_reviews(request, slug):
    product = Product.objects.get(slug=slug)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    reviews_data = []
    for review in reviews:
        reviews_data.append({
            'user': {
                'username': review.user.username,
            },
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at,
        })
    return JsonResponse({'reviews': reviews_data})

@csrf_exempt
def add_to_cart(request, product_id):
    if request.method == 'POST':
        direct_purchase = request.POST.get('direct_purchase', False)
        cart = request.session.get('cart', [])
        cart.append(product_id)
        request.session['cart'] = cart
        if direct_purchase:
            request.session['cart'] = [product_id]
            return JsonResponse({'success': True, 'length': len(cart), 'direct_purchase': True})
        return JsonResponse({'success': True, 'length': len(cart)})

@csrf_exempt
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        cart.remove(product_id)
        request.session['cart'] = cart
        return JsonResponse({'success': True, 'length': len(cart)})

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        
        try:
            line_items = []
            for product_id in cart:
                product = Product.objects.get(id=product_id)
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product.name,
                            'description': product.description,
                        },
                        'unit_amount': int(product.price * 100),
                    },
                    'quantity': 1,
                })
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                metadata={
                    'user_id': request.user.id,
                    'products': str(cart),
                },
                success_url='http://localhost:8000/cart/success',
                cancel_url='http://localhost:8000/cart',
            )
            if request.user.is_authenticated:
                return JsonResponse({'url': checkout_session.url})
            else:
                return JsonResponse({'error': 'User not authenticated'}, status=401)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        products = session['metadata']['products']
        try:
            dump_products = json.loads(products)
            for product_id in dump_products:
                Order.objects.create(user_id=user_id, product_id=product_id)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)

        request.session['cart'] = [] 

    return JsonResponse({'status': 'success'}, status=200)