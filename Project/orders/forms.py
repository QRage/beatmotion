from django import forms
from django.utils.translation import gettext_lazy as _


class OrderCreateForm(forms.Form):
    full_name = forms.CharField(label=_("Full Name"), max_length=100)
    phone = forms.CharField(label=_("Phone Number"), max_length=30)
