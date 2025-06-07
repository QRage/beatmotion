from decimal import Decimal

from django.conf import settings

from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            pid = str(product.id)
            cart_item = cart.get(pid)
            if cart_item is not None:
                cart_item["product"] = product
                # Перевіримо чи є price — якщо ні, додамо
                if "price" not in cart_item:
                    cart_item["price"] = str(product.price)

        for item in cart.values():
            print("DEBUG ITEM:", item)
            try:
                item["price"] = Decimal(item["price"])
            except KeyError:
                item["price"] = Decimal('0.00')
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
