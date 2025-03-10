from django import forms
from .models import Review

class CreateReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        labels = {
            'rating': 'Rating',
            'review_text': 'Review'
        }
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'description': forms.Textarea(attrs={'rows': 5})
        }

from django import forms
from django.core.validators import MinLengthValidator

class GlobalSearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '🔍 Search...',
            'class': 'search-input',
        }),
    )