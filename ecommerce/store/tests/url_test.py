from django.test import TestCase
from django.urls import reverse


class UrlsTestCase(TestCase):
    def test_store_url(self):
        url = reverse('store')
        self.assertEqual(url, '/')

    def test_product_info_url(self):
        url = reverse('product-info', kwargs={'product_slug': 'test-product'})
        self.assertEqual(url, '/product/test-product/')

    def test_list_category_url(self):
        url = reverse('list-category', kwargs={'category_slug': 'test-category'})
        self.assertEqual(url, '/search/test-category/')

    def test_product_review_url(self):
        url = reverse('product-review', kwargs={'product_id': 1})
        self.assertEqual(url, '/product-review/1/')

    def test_edit_review_url(self):
        url = reverse('edit-review', kwargs={'product_slug': 'test-product', 'review_id': 1})
        self.assertEqual(url, '/edit-review/test-product/1/')

    def test_search_results_url(self):
        url = reverse('search-results')
        self.assertEqual(url, '/search/')

    def test_check_new_messages_url(self):
        url = reverse('check_new_messages')
        self.assertEqual(url, '/check-new-messages/')

    def test_review_delete_url(self):
        url = reverse('review-delete', kwargs={'product_slug': 'test-product', 'pk': 1})
        self.assertEqual(url, '/review/test-product/1/delete/')