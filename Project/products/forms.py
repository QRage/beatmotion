from django import forms
from .models import Product
from .widgets import MultiFileInput


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'article', 'price', 'in_stock']

class MultiImageForm(forms.Form):
    images = forms.FileField(
        widget=MultiFileInput,
        required=False
    )
        