from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .forms import ProductForm, MultiImageForm

from .models import ProductImage, Product


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        image_form = MultiImageForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')

        if form.is_valid():
            product = form.save()

            for f in files:
                ProductImage.objects.create(product=product, image=f)

            return redirect('product_list')

    else:
        form = ProductForm()
        image_form = MultiImageForm()

    return render(request, 'products/add_product.html', {
        'form': form,
        'image_form': image_form
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {
        'products': products
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {
        'product': product
    })
