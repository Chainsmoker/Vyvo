from django.core.management.base import BaseCommand
from apps.shop.models import Product, ProductImage
from apps.shop.models import Category
from apps.accounts.models import User
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Create products'
    
    def handle(self, *args, **kwargs):
        fake = Faker()
        file = '/products_files/product-img1.png'
        images = [
            '/products_images/1.png',
            '/products_images/2.png',
            '/products_images/3.png',
            '/products_images/4.png',
            '/products_images/5.png',
            '/products_images/6.png',
            '/products_images/7.png',
            '/products_images/8.png',
            '/products_images/9.png',
            '/products_images/10.png',
            '/products_images/11.png',
            '/products_images/12.png',
            '/products_images/13.png',
        ]
        names = [
            "TaskManager Vue",
            "Booking System Django",
            "Analytics Admin Panel",
            "Marketplace Laravel",
            "Inventory Tracker Node",
            "Social Network MERN",
            "Landing Page Builder",
            "Helpdesk Ticketing System",
            "Learning Platform Angular",
            "Restaurant POS System",
            "Real Estate Listings App",
            "Subscription Billing API",
            "Crypto Wallet Starter"
        ]
        users = User.objects.all()
        categories = Category.objects.all()

        for i in range(90):
            product = Product.objects.create(
                name=random.choice(names),
                slug=fake.slug(),
                price=fake.random_int(min=1, max=100),
                description=fake.text(),
                file=file,
                creator=users[fake.random_int(min=0, max=users.count() - 1)],
                category=categories[fake.random_int(min=0, max=categories.count() - 1)],
            )
            ProductImage.objects.create(product=product, image=random.choice(images))
            self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
        