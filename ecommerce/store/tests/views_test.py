from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product, ProductReview, Category
from messaging.models import Message
from django.contrib.auth.models import User
from store.forms import ProductReviewForm

class ProductReviewCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a test product
        cls.product = Product.objects.create(title='Test Product', price=10)
        # URL for creating a review for the test product
        cls.url = reverse('product-review', kwargs={'product_id': cls.product.pk})
        # Valid form data
        cls.valid_form_data = {
            'rating': 5,
            'content': 'This is a test review.',
        }

    def test_review_submission(self):
        # Log in as the test user
        self.client.login(username='testuser', password='testpassword')
        # Submit a review for the test product
        response = self.client.post(self.url, self.valid_form_data, follow=True)
        # Check that the review was successfully submitted
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Review submitted successfully.')
        # Check that the review is saved in the database
        self.assertTrue(ProductReview.objects.filter(product=self.product, author=self.user).exists())



class ReviewUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a test product
        cls.product = Product.objects.create(title='Test Product', price=10)
        # Create a test review by the user
        cls.review = ProductReview.objects.create(product=cls.product, author=cls.user, rating=5, content='Initial review content')

    def setUp(self):
        # Initialize the test client
        self.client = Client()


    def test_displays_form_if_logged_in(self):
        # Log in as the test user
        self.client.login(username='testuser', password='testpassword')
        # Test that the view displays the review update form if the user is logged in
        url = reverse('edit-review', kwargs={'product_slug': self.product.slug, 'review_id': self.review.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/edit-review.html')
        self.assertIsInstance(response.context['form'], ProductReviewForm)

    def test_updates_review_if_author(self):
        # Log in as the test user
        self.client.login(username='testuser', password='testpassword')
        # Test that the review is updated if the user is the author of the review
        url = reverse('edit-review', kwargs={'product_slug': self.product.slug, 'review_id': self.review.pk})
        response = self.client.post(url, {'rating': 4, 'content': 'Updated review content'})
        self.assertEqual(response.status_code, 302)  # Check if redirected after successful form submission
        updated_review = ProductReview.objects.get(pk=self.review.pk)
        self.assertEqual(updated_review.rating, 4)
        self.assertEqual(updated_review.content, 'Updated review content')

    def test_does_not_update_review_if_not_author(self):
        # Create another user
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        # Log in as the other user
        self.client.login(username='otheruser', password='otherpassword')
        # Test that the review is not updated if the user is not the author of the review
        url = reverse('edit-review', kwargs={'product_slug': self.product.slug, 'review_id': self.review.pk})
        response = self.client.post(url, {'rating': 4, 'content': 'Updated review content'})
        # Check if the response contains the error message
        self.assertContains(response, 'You are not authorized to update this review.')
        # Check that the review content remains unchanged
        unchanged_review = ProductReview.objects.get(pk=self.review.pk)
        self.assertEqual(unchanged_review.rating, 5)
        self.assertEqual(unchanged_review.content, 'Initial review content')



class StoreViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a test category
        cls.category = Category.objects.create(name='Test Category', slug='test-category')
        # Create a test product
        cls.product = Product.objects.create(title='Test Product', price=10, category=cls.category)
        # Create a test product review
        cls.review = ProductReview.objects.create(product=cls.product, author=cls.user, rating=5, content='Test Review')

    def test_store_view(self):
        response = self.client.get(reverse('store'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/store.html')

    def test_list_category_view(self):
        response = self.client.get(reverse('list-category', kwargs={'category_slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/list-category.html')

    def test_product_info_view(self):
        response = self.client.get(reverse('product-info', kwargs={'product_slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product-info.html')



class CheckUnreadMessagesTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_has_unread_messages(self):
        # Create an unread message for the test user
        unread_message = Message.objects.create(sender=self.user, receiver=self.user, subject='Test', body='Test message', read_receiver=False)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('check_new_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['has_unread_messages'], True)

    def test_no_unread_messages(self):
        # Log in as the test user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('check_new_messages'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['has_unread_messages'], False)