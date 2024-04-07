
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import CreateUserForm, LoginForm, PostFormSet, UpdateUserForm, CreateProductForm


from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate


from django.contrib.auth.decorators import login_required


from django.contrib import messages


# class based views imports
from django.views.generic.edit import FormView, CreateView
from store.models import Product, Category

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
import json
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.views.generic import DeleteView

@method_decorator(login_required(login_url='my-login'), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class CreateProductView(CreateView):
    """Create a new product class based view"""
    
    model = Product
    form_class = CreateProductForm  # Your custom form for product data
    template_name = 'account/add-product.html'

    success_url = 'dashboard'

    def form_valid(self, form):

        form.instance.user = self.request.user
        product = form.save(commit=False)

        

        context = self.get_context_data()
        formset = context['formset']

       

        if formset.is_valid() and form.is_valid:
            product.save()

            for image_form in formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.product = product
                    image.save()

            messages.success(self.request, "The product was added successfully.")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


        
    def form_invalid(self, form):
        messages.error(self.request, "Failed to add the product.")
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.all()
        subcategories_data = {category.id: list(category.sub_categories.values('id', 'name')) for category in categories}
        
        context['subcategories_data'] = json.dumps(subcategories_data)
        print(subcategories_data)

        if self.request.POST:
            formset = PostFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            formset = PostFormSet(instance=self.object)

        context['formset'] = formset
        return context

    


@method_decorator(login_required(login_url='my-login'), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class UserProductsView(LoginRequiredMixin, ListView):
    """User products list class based view
    """
    model = Product
    template_name = 'account/my-products.html'
    context_object_name = 'my_products'
    paginate_by = 50

    def get_queryset(self):
        # Get the current logged-in user
        current_user = self.request.user
        # Filter products by the current user
        my_products = Product.objects.filter(user=current_user)

        sort_by = self.request.GET.get('sort_by', 'title')

        if sort_by == 'reviews':
            all_my_products = my_products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        else:
            all_my_products = my_products.order_by(sort_by)

        return all_my_products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['object_list'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['my_products'] = page_obj
        return context



@method_decorator(login_required(login_url='my-login'), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class UserProductUpdateView(UpdateView):
    """Product update class based view
    """
    model = Product
    form_class = CreateProductForm
    template_name = 'account/update-product.html'

    success_url = 'dashboard'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            formset = PostFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            formset = PostFormSet(instance=self.object)
        formset_count = formset.total_form_count()
        context['formset'] = formset
        context['formset_count'] = formset_count
        
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        product = form.save(commit=False)

        context = self.get_context_data()
        formset = context['formset']

   

        if formset.is_valid():
            product.save()
            for image_form in formset:
                if image_form.cleaned_data.get('DELETE'):
                    print("de;etiomns")
                    # Delete the image from the model
                    if image_form.instance.pk:  # Ensure instance exists
                        image_form.instance.delete()
                elif image_form.cleaned_data:  # Save new or changed images
                    image = image_form.save(commit=False)
                    image.product = product
                    image.save()

            messages.success(self.request, "The product was added successfully.")
            return super().form_valid(form)
        else:
           
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        
        messages.error(self.request, "Failed to add the product. Please check the formset.")
        return super().form_invalid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy(self.success_url)
    
    def get_object(self, queryset=None):
        return Product.objects.get(slug=self.kwargs['slug'])

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('dashboard')  # URL to redirect to after successful deletion

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()  # Delete the product from the database
        messages.success(request, "The product was deleted successfully.")
        return redirect(success_url)

def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid(): 

            user = form.save()

            user.is_active = False

            user.save()

            # Email verification setup (template)

            current_site = get_current_site(request)

            subject = 'Account verification email'
            

            message = render_to_string('account/registration/email-verification.html', {
            
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            
            })

            user.email_user(subject=subject, message=message)


            return redirect('email-verification-sent')



    context = {'form':form}


    return render(request, 'account/registration/register.html', context=context)




def email_verification(request, uidb64, token):

    # uniqueid

    unique_id = force_str(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=unique_id)
    
    # Success

    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True

        user.save()

        return redirect('email-verification-success')


    # Failed 

    else:

        return redirect('email-verification-failed')



def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')


def email_verification_success(request):

    return render(request, 'account/registration/email-verification-success.html')



def email_verification_failed(request):

    return render(request, 'account/registration/email-verification-failed.html')



def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")


    context = {'form':form}

    return render(request, 'account/my-login.html', context=context)


# logout

def user_logout(request):

    try:

        for key in list(request.session.keys()):

            if key == 'session_key':

                continue

            else:

                del request.session[key]


    except KeyError:

        pass


    messages.success(request, "Logout success")

    return redirect("store")




@login_required(login_url='my-login')
def dashboard(request):


    return render(request, 'account/dashboard.html')




@login_required(login_url='my-login')
def profile_management(request):    

    # Updating our user's username and email

    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():

            user_form.save()

            messages.info(request, "Update success!")

            return redirect('dashboard')

   

    context = {'user_form':user_form}

    return render(request, 'account/profile-management.html', context=context)




@login_required(login_url='my-login')
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':

        user.delete()


        messages.error(request, "Account deleted")


        return redirect('store')


    return render(request, 'account/delete-account.html')







 











