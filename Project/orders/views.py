from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .models import Order
from .forms import OrderCreateForm
from cart.cart_logic import Cart
from users.models import CustomUser

def order_create(request):
    cart = Cart(request)

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            user = None
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')

            if request.user.is_authenticated:
                user = request.user
                order.user = user
                if not order.email:
                    order.email = request.user.email
                if not order.phone:
                    order.phone = request.user.phone
            else:
                if phone:
                    try:
                        user = CustomUser.objects.get(phone=phone)
                    except ObjectDoesNotExist:
                        pass

                if not user and email:
                    try:
                        user = CustomUser.objects.get(email=email)
                    except ObjectDoesNotExist:
                        pass

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


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'orders/my_orders.html', {'orders': orders})
