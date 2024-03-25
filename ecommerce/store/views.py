from django.shortcuts import render
from django.urls import reverse_lazy

from . models import Category, Product, ProductReview
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .forms import ProductReviewForm
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.db.models import Q
from django.views.generic import ListView, View
from django.core.paginator import Paginator
from django.http import JsonResponse

from messaging.models import Message

class ProductReviewCreateView(LoginRequiredMixin, CreateView):
    model = ProductReview
    form_class = ProductReviewForm
    template_name = 'store/product-review.html'
    success_url = reverse_lazy('store')  # Adjust this URL name based on your project

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product_id = self.kwargs['product_id']
        # You can directly access the rating from the form data
        form.instance.rating = int(self.request.POST.get('rating'))
        messages.success(self.request, 'Review submitted successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error submitting review. Please check your input.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_id'] = self.kwargs['product_id']
        return context
    

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductReview
    form_class = ProductReviewForm
    template_name = 'store/edit-review.html'
    success_url = reverse_lazy('store')  # Replace with the URL to redirect after successful update

    def get_object(self, queryset=None):
        # Get the review object based on the provided review ID
        review_id = self.kwargs['review_id']
        return get_object_or_404(ProductReview, pk=review_id)

    def form_valid(self, form):
        # Ensure the current user is the author of the review
        if form.instance.author == self.request.user:
            messages.success(self.request, 'Review updated successfully.')
            return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, 'Failed to update review. Please check your input.')
        return super().form_invalid(form)


    
def store(request):

    all_products = Product.objects.order_by('title')
    paginator = Paginator(all_products, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'my_products':page_obj}

    return render(request, 'store/store.html', context)



def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}



def list_category(request, category_slug=None):

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)


    return render(request, 'store/list-category.html', {'category':category, 'products':products})



def product_info(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)
    reviews = ProductReview.objects.filter(product=product)

    context = {'product': product, 'reviews': reviews}

    return render(request, 'store/product-info.html', context)



class ProductSearch(ListView):
    model = Product
    template_name = 'store/search-results.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Product.objects.filter(title__icontains=query).select_related('category')
        return Product.objects.none()



def check_unread_messages(request):

    has_unread_messages = Message.objects.filter(receiver=request.user, read_receiver=False).exists()
    return JsonResponse({'has_unread_messages': has_unread_messages})