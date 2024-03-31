# your_app/management/commands/populate_products.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from store.models import Product, Category, ProductReview  # Import ProductReview model
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populates the database with sample products and reviews'

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
                slug=slugify(title)
            )
            products_to_create.append(product)

        # Bulk create products
        created_products = Product.objects.bulk_create(products_to_create)

        # Create reviews for each product
        reviews_to_create = []
        for product in created_products:
            num_reviews = random.randint(1, 10)  # Random number of reviews per product
            for _ in range(num_reviews):
                review = ProductReview(
                    product=product,
                    author=random.choice(users),
                    rating=random.randint(1, 5),
                    content=fake.paragraph()
                )
                reviews_to_create.append(review)

        # Bulk create reviews
        ProductReview.objects.bulk_create(reviews_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(products_to_create)} products and {len(reviews_to_create)} reviews'))
