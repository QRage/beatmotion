from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart_logic import Cart


def order_create(request):
    cart = Cart(request)

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            order.add_items_from_cart(cart)

            cart.clear()
            request.session['order_id'] = order.id

            return redirect(reverse('orders:order_success'))
    else:
        form = OrderCreateForm()

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
    })


def order_success(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    del request.session['order_id']
    return render(request, 'orders/order_success.html', {'order': order})
