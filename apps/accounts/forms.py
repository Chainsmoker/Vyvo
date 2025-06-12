from django import forms 
from allauth.account.forms import SignupForm
from .models import User

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    agree = forms.BooleanField(required=False)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1.strip()) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if len(password2.strip()) < 8:
            raise forms.ValidationError('La contraseña debe tener al menos 8 caracteres')
        if password2 != password1:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2
    
    def clean_agree(self):
        agree = self.cleaned_data.get('agree')
        if not agree:
            raise forms.ValidationError('Debes aceptar los términos y condiciones')
        return agree

    def save(self, request):
        user = super().save(request)
        username = self.cleaned_data.get('username')
        user.username = username.lower()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'facebook', 'twitter', 'phone', 'profile_picture', 'banner_picture']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditProfileForm, self).__init__(*args, **kwargs)
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name.strip()) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name.strip()) < 2:
            raise forms.ValidationError("El apellido debe tener al menos 2 caracteres.")
        return last_name
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if username == self.user.username:
            return username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone and not phone.startswith('+'):
            raise forms.ValidationError("El número de teléfono debe comenzar con un signo más (+).")
        return phone
    
    def clean_facebook(self):
        facebook = self.cleaned_data['facebook']
        if facebook and not facebook.startswith('https://www.facebook.com/'):
            raise forms.ValidationError("El enlace debe ser un enlace válido de Facebook.")
        return facebook

    def clean_twitter(self):
        twitter = self.cleaned_data['twitter']
        if twitter and not twitter.startswith('https://twitter.com/'):
            raise forms.ValidationError("El enlace debe ser un enlace válido de Twitter.")
        return twitter
        