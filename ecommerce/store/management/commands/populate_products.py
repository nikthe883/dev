# your_app/management/commands/populate_products.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from store.models import Product, Category
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populates the database with sample products'

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories = Category.objects.all()
        users = User.objects.all()
        
        products_to_create = []

        for _ in range(100): 
            category = random.choice(categories)
            user = random.choice(users)
            title = fake.word()
            brand = fake.company()
            description = fake.paragraph()
            price = round(random.uniform(1, 1000), 2)
            product = Product(
                category=category,
                title=title,
                brand=brand,
                description=description,
                price=price,
                user=user,
                slug=title
            )
            products_to_create.append(product)

        # Bulk create products
        Product.objects.bulk_create(products_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(products_to_create)} products'))