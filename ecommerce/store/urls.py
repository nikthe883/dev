from django.urls import path
from .views import ProductReviewCreateView, ReviewUpdateView, ReviewDeleteView, ProductSearch
from . import views

urlpatterns = [
    # Store main page
    path('', views.store, name='store'),

    # Individual product
    path('product/<slug:product_slug>/', views.product_info, name='product-info'),

    # Individual category
    path('search/<slug:category_slug>/', views.list_category, name='list-category'),

    # Create product review
    path('product-review/<int:product_id>/', ProductReviewCreateView.as_view(), name='product-review'),

    # Edit product review
    path('edit-review/<slug:product_slug>/<int:review_id>/', ReviewUpdateView.as_view(), name='edit-review'),

    # Search results
    path('search/', ProductSearch.as_view(), name='search-results'),  

    # Check for new messages
    path('check-new-messages/', views.check_unread_messages, name='check_new_messages'),

    # Delete product review
    path('review/<slug:product_slug>/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]











