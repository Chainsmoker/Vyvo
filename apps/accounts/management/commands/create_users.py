from django.core.management.base import BaseCommand
from apps.accounts.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker

class Command(BaseCommand):
    help = 'Create users'
    
    def handle(self, *args, **kwargs):
        fake = Faker()
        for i in range(5):
            username = fake.user_name()
            User.objects.create_user(
                username=username,
                email=f'{username}@gmail.com',
                password=make_password('password123'),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_creator=True,
                bio=fake.text(),
                phone=fake.phone_number(),
                facebook=fake.url(),
                twitter=fake.url(),
                pinterest=fake.url(),
                instagram=fake.url(),
            )
        
            self.stdout.write(self.style.SUCCESS(f'Successfully created user {username}'))
        