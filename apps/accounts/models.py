from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.db.models import Avg

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures', default='/profile_pictures/default.avif')
    banner_picture = models.ImageField(upload_to='banner_pictures', blank=True, null=True)
    is_creator = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True, validators=[
        MinLengthValidator(10, message="El texto debe tener al menos 10 caracteres"),
        MaxLengthValidator(500, message="El texto debe tener menos de 500 caracteres")
    ])
    phone = models.CharField(max_length=15, blank=True, null=True, validators=[
        RegexValidator(r'^\+?1?\d{10,15}$', message="El número debe tener entre 10 y 15 dígitos")
    ])

    facebook = models.URLField(blank=True, null=True, validators=[
        RegexValidator(r'^https://www\.facebook\.com/[^/]+$', message="El enlace debe ser un enlace válido de Facebook")
    ])
    twitter = models.URLField(blank=True, null=True, validators=[
        RegexValidator(r'^https://twitter\.com/[^/]+$', message="El enlace debe ser un enlace válido de Twitter")
    ])
    pinterest = models.URLField(blank=True, null=True, validators=[
        RegexValidator(r'^https://pinterest\.com/[^/]+$', message="El enlace debe ser un enlace válido de Pinterest")
    ])
    instagram = models.URLField(blank=True, null=True, validators=[
        RegexValidator(r'^https://instagram\.com/[^/]+$', message="El enlace debe ser un enlace válido de Instagram")
    ])

    follows = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False)
    
    def get_profile_image(self):
        if self.profile_picture:
            return self.profile_picture.url

    def get_cover_image(self):
        if self.banner_picture:
            return self.banner_picture.url

    def get_average_rating(self):
        rating = self.products.aggregate(Avg('reviews__rating'))['reviews__rating__avg'] 
        rating = int(rating) if rating else 0
        return rating

    def fill_stars(self):
        stars = self.get_average_rating()
        return '<li class="star-rating__item font-11"><i class="fas fa-star"></i></li>' * stars + '<li class="star-rating__item font-11"><i class="far fa-star"></i></li>' * (5 - stars)