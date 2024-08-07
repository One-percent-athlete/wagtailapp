from django import forms

from .models import Review

REVIEW_CHOICES = [
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author', 'text', 'rating']
        widgets = {
            forms.RadioSelect(
                choices=REVIEW_CHOICES
            )
        }

class SearchForm(forms.Form):
    query = forms.CharField()