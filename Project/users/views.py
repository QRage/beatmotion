from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_backends, update_session_auth_hash, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError
from django.views import View

from .forms import UserUpdateForm, CustomUserCreationForm


@login_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)

            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                update_session_auth_hash(request, user)

            user.save()
            messages.success(request, _("Your profile has been updated."))
            return redirect("users:profile")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/profile.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                backend = get_backends()[0]
                login(request, user, backend=backend.__module__ + '.' + backend.__class__.__name__)
                return redirect("profile")
            except IntegrityError:
                form.add_error(None, _("A user with this username or email already exists."))
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


class LogoutGetView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
