from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, Category

class ShopView(ListView):
    template_name = "shop.html"
    model = Product
    context_object_name = "products"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:12]
        return context

class ProductView(DetailView):
    template_name = "product-details.html"
    model = Product
    context_object_name = "product"

class CartView(TemplateView):
    template_name = "cart.html"