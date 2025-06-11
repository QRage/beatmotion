from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from .models import CustomUser


class UserUpdateForm(forms.ModelForm):
    new_password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Leave blank if you don't want to change the password."),
    )
    confirm_password = forms.CharField(
        label=_("Confirm password"),
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone']
        labels = {
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'email': _("Email"),
            'phone': _("Phone number"),
        }

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')

        if pwd or confirm:
            if pwd != confirm:
                raise forms.ValidationError(_("Passwords do not match."))
            password_validation.validate_password(pwd, self.instance)

        return cleaned_data


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError(_("This username is already taken."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email is already registered."))
        return email
