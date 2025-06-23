from django.db import models
from django.db.models import Avg
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator, MaxLengthValidator, MaxValueValidator
from apps.accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='categories_icons/')
    image = models.ImageField(upload_to='categories_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return self.image.url
        return '/static/assets/img/product/collection/product-collection-1.jpg'

    def get_products_count(self):
        return self.products.count()

class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
        
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(validators=[MinLengthValidator(3), MaxLengthValidator(300)])
    created_at = models.DateTimeField(auto_now_add=True)

    def fill_stars(self):
        return '<li class="star-rating__item font-11"><i class="fas fa-star"></i></li>' * self.rating + '<li class="star-rating__item font-11"><i class="far fa-star"></i></li>' * (5 - self.rating)
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, 
        validators=[
            MinValueValidator(1), 
            RegexValidator(
                regex='^[0-9]+(\.[0-9]{2})?$', 
                message='Ingresa un precio válido, ejemplo: 10.00'
                )
            ]
        )
    description = models.TextField(validators=[MinLengthValidator(10), MaxLengthValidator(1000)])
    file = models.FileField(upload_to='products_files/')
    #tags = models.ManyToManyField(Tag, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_favorites_count(self):
        return self.favorites.count()

    def get_featured_image(self):
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return None
    
    def get_images(self):
        return self.images.all()

    def get_average_rating(self):
        return int(self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0)

    def fill_stars(self):
        return '<li class="star-rating__item font-11"><i class="fas fa-star"></i></li>' * self.get_average_rating() + '<li class="star-rating__item font-11"><i class="far fa-star"></i></li>' * (5 - self.get_average_rating())

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products_images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    
class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"