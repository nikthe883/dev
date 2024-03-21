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

        for _ in range(1000):  # Change 1000 to the number of products you want to create
            category = random.choice(categories)
            user = random.choice(users)
            title = fake.text(max_nb_chars=50)
            brand = fake.company()
            description = fake.paragraph()
            price = round(random.uniform(1, 1000), 2)
            product = Product.objects.create(
                category=category,
                title=title,
                brand=brand,
                description=description,
                price=price,
                user=user
            )
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product}'))
