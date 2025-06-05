from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Product, Category
from .widgets import MultiFileInput


class ProductForm(forms.ModelForm):
    category = forms.CharField(
        required=False,
        label=_("Category"),
        help_text=_("Enter category name")
    )

    class Meta:
        model = Product
        fields = ['title', 'description', 'price']


class MultiImageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'] = forms.FileField(
            widget=MultiFileInput(attrs={"multiple": True}),
            required=False,
            label=_("Product images")
        )
