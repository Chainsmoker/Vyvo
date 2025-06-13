from .models import Category

def get_categories(request):
    categories = Category.objects.all()[:5]
    return {'categories_footer': categories}