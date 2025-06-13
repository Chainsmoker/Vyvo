from django.views.generic import TemplateView
from apps.shop.models import Product

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_products'] = Product.objects.all()[:12]
        context['featured_products'] = Product.objects.all()[:4]
        context['new_products'] = Product.objects.all()[:8]
        return context

class ContactView(TemplateView):
    template_name = "contact.html"
    