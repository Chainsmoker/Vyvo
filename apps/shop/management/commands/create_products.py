from django.core.management.base import BaseCommand
from apps.shop.models import Product, ProductImage
from apps.shop.models import Category
from apps.accounts.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Create products'
    
    def handle(self, *args, **kwargs):
        fake = Faker()
        file = '/products_files/product-img1.png'
        images = [
            '/products_images/product-img1.png',
            '/products_images/product-img2.png',
            '/products_images/product-img3.png',
            '/products_images/product-img4.png',
            '/products_images/product-img5.png',
            '/products_images/product-img6.png',
            '/products_images/product-img7.png',
            '/products_images/product-img8.png',
            '/products_images/product-img9.png',
            '/products_images/product-img10.png',
            '/products_images/product-img11.png',
            '/products_images/product-img12.png',
            '/products_images/product-img13.png',
            '/products_images/product-img14.png',
        ]
        names = [
            "Dev Portfolio Pro",
            "Ecommerce React",
            "SaaS Dashboard Kit",
            "TaskManager Vue",
            "Blogify NextJS",
            "CRM Express",
            "ChatApp Flutter",
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
            "Fitness Tracker Mobile",
            "Crypto Wallet Starter"
        ]
        users = User.objects.all()
        categories = Category.objects.all()

        for i in range(5):
            product = Product.objects.create(
                name=names[i],
                slug=fake.slug(),
                price=fake.random_int(min=1, max=100),
                description=fake.text(),
                file=file,
                creator=users[fake.random_int(min=0, max=users.count() - 1)],
                category=categories[fake.random_int(min=0, max=categories.count() - 1)],
            )
            ProductImage.objects.create(product=product, image=images[fake.random_int(min=0, max=13)])
            self.stdout.write(self.style.SUCCESS(f'Created product: {names[i]}'))
        