from django import forms
from .models import Product, ProductImage, Review

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class CreateProductForm(forms.ModelForm):
    images = MultipleFileField(required=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price','category', 'file', 'images']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CreateProductForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if tags:
            if ',' in tags:
                tags = tags.split(',')
                tags = [tag.strip() for tag in tags]
                self.cleaned_data['tags'] = tags
            else:
                self.cleaned_data['tags'] = [tags.strip()]
        else:
            raise forms.ValidationError('Debes ingresar al menos un tag')

        return self.cleaned_data['tags']

    def clean_images(self):
        images = self.cleaned_data['images']
        if not images:
            raise forms.ValidationError("Debes seleccionar al menos una imagen.")
        if len(images) > 4:
            raise forms.ValidationError("Se pueden subir hasta 4 imÃ¡genes.")
        return images

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']