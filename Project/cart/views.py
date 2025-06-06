from django.shortcuts import render, redirect
from products.models import Product


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
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    
    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]['quantity']
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })
