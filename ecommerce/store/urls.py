
from django.urls import path

from .views import ProductReviewCreateView,ReviewUpdateView

from . import views
from .views import ProductSearch

urlpatterns = [


    # Store main page

    path('', views.store, name='store'),


    # Individual product

    path('product/<slug:product_slug>/', views.product_info, name='product-info'),


    # Individual category

    path('search/<slug:category_slug>/', views.list_category, name='list-category'),

    path('product-review/<int:product_id>/', ProductReviewCreateView.as_view(), name='product-review'),

    path('edit-review/<int:review_id>/', ReviewUpdateView.as_view(), name='edit-review'),

    path('search/', ProductSearch.as_view(), name='search-results'),  


]














