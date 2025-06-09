from django.shortcuts import render, redirect

from products.models import Product
from .cart_logic import Cart


def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'quantity': 1}
    request.session['cart'] = cart
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    cart_items = list(cart)
    total = cart.get_total_price()

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })
