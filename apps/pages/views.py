from django.views.generic import TemplateView
from apps.shop.models import Product, Category

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_products'] = {
            'wp': Product.objects.filter(category__name='WordPress').order_by('-created_at')[:12],
            'laravel': Product.objects.filter(category__name='Laravel').order_by('-created_at')[:12],
            'php': Product.objects.filter(category__name='PHP').order_by('-created_at')[:12],
            'html': Product.objects.filter(category__name='HTML').order_by('-created_at')[:12],
            'sketch': Product.objects.filter(category__name='Sketch').order_by('-created_at')[:12],
            'figma': Product.objects.filter(category__name='Figma').order_by('-created_at')[:12],
            'bootstrap': Product.objects.filter(category__name='Bootstrap').order_by('-created_at')[:12],
            'flutter': Product.objects.filter(category__name='Flutter').order_by('-created_at')[:12],
            'react': Product.objects.filter(category__name='React').order_by('-created_at')[:12],
        }
        context['featured_products'] = Product.objects.all()[:4]
        context['new_products'] = Product.objects.all()[:8]
        context['categories'] = Category.objects.all()
        return context

class ContactView(TemplateView):
    template_name = "contact.html"
    