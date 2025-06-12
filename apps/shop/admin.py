from django.contrib import admin
from .models import Product, Category, Tag, Review, ProductImage, FavoriteProduct

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Review)
admin.site.register(ProductImage)
admin.site.register(FavoriteProduct)
