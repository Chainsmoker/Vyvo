from django.views.generic import FormView, DetailView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from apps.shop.models import Review, Category
from apps.shop.forms import CreateProductForm
from .models import User
from .forms import CustomSignupForm, EditProfileForm

@method_decorator(csrf_exempt, name='dispatch')
class ProfileView(DetailView):
    template_name = "profile.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.get_object() == self.request.user
        context['edit_profile_form'] = EditProfileForm(instance=self.get_object(), user=self.request.user)
        context['reviews'] = Review.objects.filter(product__creator=self.get_object()).exclude(user=self.get_object())
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = EditProfileForm(request.POST, request.FILES, instance=self.object, user=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            sanitized_errors = {
                field: error[0] for field, error in form.errors.items()
            }
            return JsonResponse({'success': False, 'errors': sanitized_errors})

class SignupView(FormView):
    template_name = "account/signup.html"
    form_class = CustomSignupForm
    success_url = 'account_login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('pages:index')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.save(self.request)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('account_login') + '?register=success'