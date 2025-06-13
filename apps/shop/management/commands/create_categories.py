from django.core.management.base import BaseCommand
from apps.shop.models import Category

class Command(BaseCommand):
    help = 'Create categories'
    
    def handle(self, *args, **kwargs):
        names = ['WordPress', 'Laravel', 'PHP', 'HTML', 'Sketch', 'Figma', 'Bootstrap', 'Tailwind', 'React']
        icons = ['/static/assets/images/thumbs/tech-icon-white1.png', '/static/assets/images/thumbs/tech-icon-white2.png', '/static/assets/images/thumbs/tech-icon-white3.png', '/static/assets/images/thumbs/tech-icon-white4.png', '/static/assets/images/thumbs/tech-icon-white5.png', '/static/assets/images/thumbs/tech-icon-white6.png', '/static/assets/images/thumbs/tech-icon-white7.png', '/static/assets/images/thumbs/tech-icon-white8.png', '/static/assets/images/thumbs/tech-icon-white9.png']

        for name, icon in zip(names, icons):
            Category.objects.create(name=name, icon=icon)
            self.stdout.write(self.style.SUCCESS(f'Created category: {name}'))