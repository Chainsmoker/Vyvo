from django.urls import path
from .views import ShopView, ProductView, CartView, create_product, create_review, get_reviews

app_name = 'shop'

urlpatterns = [
    path('shop/', ShopView.as_view(), name='products'),
    path('product/create/', create_product, name='create_product'),
    path('product/review/<str:slug>/', create_review, name='create_review'),
    path('product/reviews/<str:slug>/', get_reviews, name='get_reviews'),
    path('product/<str:slug>/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
]