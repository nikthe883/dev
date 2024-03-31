import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from store.models import Product, Category, Images, ProductReview
from faker import Faker
import random
from django.core.files import File

class Command(BaseCommand):
    help = 'Populates the database with sample products and reviews'

    def handle(self, *args, **kwargs):
        fake = Faker()
        categories = Category.objects.all()
        users = User.objects.all()
        used_titles = set()

        # Path to the directory containing the product images
        images_dir = r'F:\Downloads\testImages'

        for _ in range(100):
            category = random.choice(categories)
            user = random.choice(users)
            title = fake.unique.word()
            while title in used_titles:
                title = fake.unique.word()
            used_titles.add(title)
            brand = fake.company()
            description = fake.paragraph()
            price = round(random.uniform(1, 1000), 2)

            # Choose a random image file from the directory
            image_file = random.choice(os.listdir(images_dir))
            image_path = os.path.join(images_dir, image_file)

            # Create product instance
            product = Product.objects.create(
                category=category,
                title=title,
                brand=brand,
                description=description,
                price=price,
                user=user,
                slug=slugify(title),
            )

            # Create images for the product
            with open(image_path, 'rb') as f:
                image_name = os.path.basename(image_path)
                product_image = Images(product=product)
                product_image.image.save(image_name, File(f), save=True)

        # Create reviews for each product
        for product in Product.objects.all():
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

            # Bulk create reviews
            ProductReview.objects.bulk_create(reviews_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample products and reviews'))
