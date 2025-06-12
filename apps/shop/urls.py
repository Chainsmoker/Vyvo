from django.urls import path
from .views import ShopView, ProductView, CartView

app_name = 'shop'

urlpatterns = [
    path('shop/', ShopView.as_view(), name='products'),
    path('product/<str:slug>/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart')
]