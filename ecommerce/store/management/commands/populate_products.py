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
        titles_to_generate = 9000

        # Path to the directory containing the product images
        images_dir = r'F:\Downloads\testImages'

        for i in range(1, titles_to_generate + 1):
            title = f"{fake.unique.word()}_{i}"  # Append number to title for uniqueness
            while Product.objects.filter(title=title).exists():  # Check if title exists in the database
                i += 1
                title = f"{fake.unique.word()}_{i}"
            
            category = random.choice(categories)
            user = random.choice(users)
            brand = fake.company()
            description = fake.paragraph()
            price = round(random.uniform(1, 1000), 2)

            # Choose a random image file from the directory
            image_file = random.choice(os.listdir(images_dir))
            image_path = os.path.join(images_dir, image_file)

            # Create product instance
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

            # Print message when a product is generated
            print(f"Generated product: {title}")

            # Create images for the product
            with open(image_path, 'rb') as f:
                image_name = os.path.basename(image_path)
                product_image = Images(product=product)
                product_image.image.save(image_name, File(f), save=True)

            # Create reviews for the product
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

            # Create reviews
            ProductReview.objects.bulk_create(reviews_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample products and reviews'))
