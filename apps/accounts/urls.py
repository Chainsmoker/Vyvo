from django.urls import path
from allauth.account import views as allauth_views
from allauth.socialaccount.providers.google import views as google_views

from .views import ProfileView, SignupView

urlpatterns = [
    path('login/', allauth_views.login, name='account_login'),
    path('logout/', allauth_views.logout, name='account_logout'),
    path('register/', SignupView.as_view(), name='account_signup'),

    path('google/login/', google_views.oauth2_login, name='google_login'),
    path('google/login/callback/', google_views.oauth2_callback, name='google_callback'),

    path("profile/@<str:username>/", ProfileView.as_view(), name="profile"),
]
