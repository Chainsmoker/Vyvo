from django.views.generic import TemplateView, ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from .models import Product, Category, ProductImage, Review
from .forms import CreateProductForm, ReviewForm

class ShopView(ListView):
    template_name = "shop.html"
    model = Product
    context_object_name = "products"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('-created_at')[:12]
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