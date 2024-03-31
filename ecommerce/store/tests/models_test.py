from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product, Images, ProductReview
from django.contrib.auth.models import User


class ModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.user = User.objects.create(username='test_user')

    def test_product_creation(self):
        product = Product.objects.create(
            category=self.category,
            title='Test Product',
            brand='Test Brand',
            description='This is a test product',
            price=10.99,
            user=self.user
        )
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.average_rating, 0)  # No reviews, so average rating should be 0
        self.assertEqual(str(product), 'Test Product')

    def test_images_creation(self):
        product = Product.objects.create(
            category=self.category,
            title='Test Product',
            brand='Test Brand',
            description='This is a test product',
            price=10.99,
            user=self.user
        )
        image = Images.objects.create(
            product=product,
            image='test_image.jpg'
        )
        self.assertEqual(image.product.title, 'Test Product')

    def test_product_review_creation(self):
        product = Product.objects.create(
            category=self.category,
            title='Test Product',
            brand='Test Brand',
            description='This is a test product',
            price=10.99,
            user=self.user
        )
        review = ProductReview.objects.create(
            product=product,
            author=self.user,
            rating=4,
            content='This is a test review'
        )
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.product.title, 'Test Product')

    def test_category_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), reverse('list-category', args=['test-category']))

    def test_best_product(self):
        # Test getting the best-rated product
        product = Product.objects.create(
            category=self.category,
            title='Best Product',
            brand='Best Brand',
            description='This is the best product',
            price=99.99,
            user=self.user
        )
        review = ProductReview.objects.create(
            product=product,
            author=self.user,
            rating=5,
            content='This is a great product!'
        )
        best_product = Product.best_product()
        self.assertEqual(best_product, product)



