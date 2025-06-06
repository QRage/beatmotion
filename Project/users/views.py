from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserUpdateForm


@login_required
def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "users/profile.html", {"form": form})
