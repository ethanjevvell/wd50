from django import forms
from .models import Listing, CATEGORIES

class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    category = forms.ChoiceField(choices=CATEGORIES)
    startingBid = forms.IntegerField()
    description = forms.CharField(widget=forms.Textarea)
    imageURL = forms.URLField(required=False)