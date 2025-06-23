from django.urls import path
from .views import ShopView, ProductView, CartView, create_product, create_review, get_reviews, add_to_cart, remove_from_cart, create_checkout_session, CartSuccessView, stripe_webhook

app_name = 'shop'

urlpatterns = [
    path('shop/', ShopView.as_view(), name='products'),
    path('product/create/', create_product, name='create_product'),
    path('product/review/<str:slug>/', create_review, name='create_review'),
    path('product/reviews/<str:slug>/', get_reviews, name='get_reviews'),
    path('product/<str:slug>/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/success/', CartSuccessView.as_view(), name='cart_success'),

    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('webhook-stripe/', stripe_webhook, name='stripe_webhook'),
]