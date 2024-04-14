import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from store.models import Product, Category, Images, ProductReview
from faker import Faker
import random
from django.core.files import File

class Command(BaseCommand):
    help = 'Populates the database with sample products, categories, and reviews'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Ensure there are some users to associate with reviews and products
        if not User.objects.exists():
            self.stdout.write(self.style.ERROR('No users found. Please create some user accounts first.'))
            return
        
        users = User.objects.all()

        # Create some sample categories if none exist
        if not Category.objects.exists():
            for _ in range(10):  # Create 10 sample categories
                Category.objects.create(
                    name=fake.unique.company(),
                    slug=slugify(fake.unique.company())
                )
            self.stdout.write(self.style.SUCCESS('Sample categories created.'))
        
        categories = Category.objects.all()

        titles_to_generate = 100
        base_dir = os.path.dirname(__file__)
        images_dir = os.path.join(base_dir, 'testImages')

        if not os.path.exists(images_dir):
            self.stdout.write(self.style.ERROR('Image directory does not exist'))
            return
        if not os.listdir(images_dir):
            self.stdout.write(self.style.ERROR('No images found in the directory'))
            return

        for i in range(1, titles_to_generate + 1):
            title = f"{fake.unique.word()}_{i}"
            category = random.choice(categories)
            user = random.choice(users)
            brand = fake.company()
            description = fake.paragraph()
            price = round(random.uniform(1, 1000), 2)

            image_file = random.choice(os.listdir(images_dir))
            image_path = os.path.join(images_dir, image_file)

            product = Product(
                category=category,
                title=title,
                brand=brand,
                description=description,
                price=price,
                user=user,
                slug=slugify(title),
            )
            product.save()
            print(f"Generated product: {title}")

            with open(image_path, 'rb') as f:
                image_name = os.path.basename(image_path)
                product_image = Images(product=product)
                product_image.image.save(image_name, File(f), save=True)

            reviews_to_create = []
            num_reviews = random.randint(1, 10)
            for _ in range(num_reviews):
                review = ProductReview(
                    product=product,
                    author=random.choice(users),
                    rating=random.randint(1, 5),
                    content=fake.paragraph()
                )
                reviews_to_create.append(review)

            ProductReview.objects.bulk_create(reviews_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample products, categories, and reviews'))
