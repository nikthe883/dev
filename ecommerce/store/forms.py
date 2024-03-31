from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    """
    Form for creating or updating product reviews.
    """
    rating = forms.IntegerField(label='Rating', min_value=1, max_value=5)

    class Meta:
        model = ProductReview
        fields = ['rating', 'content']