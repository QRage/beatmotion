from django import forms
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone']
        labels = {
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'email': _("Email"),
            'phone': _("Phone number"),
        }
