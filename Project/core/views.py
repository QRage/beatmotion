from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views import View


from products.models import Product


def home_view(request):
    products = Product.objects.all()
    return render(request, 'core/home.html', {
        'products': products
    })


class LogoutGetView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')
