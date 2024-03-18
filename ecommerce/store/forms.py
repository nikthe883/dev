
from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'content']

    rating = forms.IntegerField(label='Rating', min_value=1, max_value=5)


class ProductSearchForm(forms.Form):
    query = forms.CharField(label='Search')