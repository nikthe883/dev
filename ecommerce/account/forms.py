
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms
from django.forms import ModelForm, inlineformset_factory

from django.forms.widgets import PasswordInput, TextInput

from store.models import Product, Category, Images

# Prodcut from

class CreateProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['category','title', 'brand', 'description', 'price']
   
    def clean_title(self):
        title = self.cleaned_data.get('title')
        existing_product = Product.objects.filter(title__iexact=title).exclude(pk=self.instance.pk if self.instance else None).first()

        if existing_product:
            raise forms.ValidationError('A product with this title already exists. Please choose a different title.')

        return title

class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Images
        fields = ('image', )

PostFormSet = inlineformset_factory(
    Product, Images, form=ImageForm,
     extra=2, can_delete=True
)
# Registration form

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        # Mark email as required

        self.fields['email'].required = True


    # Email validation
    
    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError('This email is invalid')

        # len function updated ###

        if len(email) >= 350:

            raise forms.ValidationError("Your email is too long")


        return email



# Login form

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())



# Update form

class UpdateUserForm(forms.ModelForm):

    password = None


    class Meta:

        model = User

        fields = ['username', 'email']
        exclude = ['password1', 'password1']
    

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        # Mark email as required

        self.fields['email'].required = True

        
    # Email validation
    
    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():

            raise forms.ValidationError('This email is invalid')

        # len function updated ###

        if len(email) >= 350:

            raise forms.ValidationError("Your email is too long")


        return email
        
        
 
 

    