from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Product, ProductReview
from .forms import ProductReviewForm
from messaging.models import Message

class ProductReviewCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a product review.

    This view allows authenticated users to submit a review for a specific product.
    """

    model = ProductReview
    form_class = ProductReviewForm
    template_name = 'store/product-review.html'
    

    def form_valid(self, form):
        """
        Handle form validation for submitting a review.

        If the form is valid, sets the author, product ID, and rating for the review,
        and displays a success message.

        Args:
            form (ProductReviewForm): The form instance.

        Returns:
            HttpResponseRedirect: Redirects to the success URL after successful form submission.
        """

        form.instance.author = self.request.user
        form.instance.product_id = self.kwargs['product_id']
        form.instance.rating = int(self.request.POST.get('rating'))
        messages.success(self.request, 'Review submitted successfully.')

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle form invalidation for submitting a review.

        If the form is invalid, displays an error message.

        Args:
            form (ProductReviewForm): The form instance.

        Returns:
            HttpResponseRedirect: Redirects to the current page.
        """

        messages.error(self.request, 'Error submitting review. Please check your input.')

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Add additional context data for the template.

        Adds the product ID to the context for use in the template.

        Returns:
            dict: Additional context data.
        """

        context = super().get_context_data(**kwargs)
        context['product_id'] = self.kwargs['product_id']

        return context
    
    def get_success_url(self):
        """
        Get the success URL after submitting a review.

        Returns:
            str: The success URL to redirect to after form submission.
        """

        product_id = self.kwargs['product_id']
        product = Product.objects.get(pk=product_id)

        return reverse_lazy('product-info', kwargs={'product_slug': product.slug})

    

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating a product review.
    Requires user authentication.
    """

    model = ProductReview
    form_class = ProductReviewForm
    template_name = 'store/edit-review.html'
    

    def get_object(self, queryset=None):
        """
        Retrieve the review object based on the provided review ID.
        """

        review_id = self.kwargs['review_id']

        return get_object_or_404(ProductReview, pk=review_id)

    def form_valid(self, form):
        """
        Process the valid form data.
        If the current user is the author of the review, save the form and display a success message.
        """
      
        if form.instance.author == self.request.user:
            messages.success(self.request, 'Review updated successfully.')

            return super().form_valid(form)
        
        else:
            messages.error(self.request, 'You are not authorized to update this review.')

            return self.form_invalid(form)


    def form_invalid(self, form):
        """
        Process the invalid form data.
        Display an error message and return the invalid form.
        """

        messages.error(self.request, 'Failed to update review. Please check your input.')

        return super().form_invalid(form)
    

    def get_success_url(self):
        """
        Get the URL to redirect to after successfully updating the review.
        """
        
        product_slug = self.kwargs['product_slug']
      
        return reverse_lazy('product-info', kwargs={'product_slug': product_slug})



class ReviewDeleteView(DeleteView):
    """
    View for deleting a product review.
    """

    model = ProductReview
    success_url = reverse_lazy('dashboard')  # URL to redirect to after successful deletion

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        """
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()  # Delete the product from the database
        messages.success(request, "The review was deleted successfully.")

        return redirect(success_url)
    
    def get_success_url(self):
        """
        Define the success URL after successfully deleting the review.
        """

        product_slug = self.kwargs['product_slug']
      
        return reverse_lazy('product-info', kwargs={'product_slug': product_slug})
    
    
class ProductSearch(ListView):
    """
    View for searching products and displaying search results.
    """

    model = Product
    template_name = 'store/search-results.html'
    context_object_name = 'search_results'
    paginate_by = 50

    def check_query(self, queryset):
        """
        Check and filter search query.
        """
 
        
        if queryset:
            # Save query in session
            self.request.session['search_query'] = queryset
        elif 'query' in self.request.GET:
            # Clear session query if an empty search is performed
            self.request.session.pop('search_query', None)

        # Retrieve query from session if available
        session_query = self.request.session.get('search_query', '')

        search_results = Product.objects.all()  # Get all products queryset

        if session_query:
            search_results = search_results.filter(title__icontains=session_query)

        return search_results

    def get_queryset(self):
        """
        Get the queryset based on search query and sorting criteria.
        """

        query = self.request.GET.get('query')

        sort_by = self.request.GET.get('sort_by', 'title')
        if query:
            search_results = self.check_query(query)
        else:
            search_results = self.check_query(None)


        if sort_by == 'reviews':
            search_results = search_results.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        else:
            search_results = search_results.order_by(sort_by)

        return search_results
        

    def get_context_data(self, **kwargs):
        """
        Add pagination information to the context.
        """

        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['search_results'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['products'] = page_obj
        return context


    
def store(request):
    """
    Render the main store page with products sorted based on the specified criteria.
    """
    
    sort_by = request.GET.get('sort_by', 'title')

    if sort_by == 'reviews':
        all_products = Product.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        all_products = Product.objects.order_by(sort_by)

    
    paginator = Paginator(all_products, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products':page_obj,
               'sort_by': sort_by,}

    return render(request, 'store/store.html', context)



def categories(request):
    """
    Get all categories and return them in the context for rendering in templates.
    """

    categories = Category.objects.all()
    return {'categories': categories}



def list_category(request, category_slug=None):
    """
    Render the page with products belonging to the specified category, sorted based on the specified criteria.
    """

    category = get_object_or_404(Category, slug=category_slug)

    products = Product.objects.filter(category=category)

    sort_by = request.GET.get('sort_by', 'title')

    if sort_by == 'reviews':
        all_category_products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    else:
        all_category_products = products.order_by(sort_by)

    
    paginator = Paginator(all_category_products, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products':page_obj,
               'sort_by': sort_by,
               'category':category,}


    return render(request, 'store/list-category.html', context)



def product_info(request, product_slug):
    """
    Render the page with detailed information about the specified product, including reviews.
    """

    product = get_object_or_404(Product, slug=product_slug)
    reviews = ProductReview.objects.filter(product=product)

    context = {'product': product, 'reviews': reviews}

    return render(request, 'store/product-info.html', context)





def check_unread_messages(request):
    """
    Check if the current user has unread messages and return the result as JSON response.
    """

    has_unread_messages = Message.objects.filter(receiver=request.user, read_receiver=False).exists()

    return JsonResponse({'has_unread_messages': has_unread_messages})