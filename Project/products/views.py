from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ProductForm, MultiImageForm
from .models import ProductImage, Product, Category


@login_required
def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST)
        image_form = MultiImageForm(request.POST, request.FILES)

        print("FILES:", request.FILES)
        images = request.FILES.getlist('images')
        print("IMAGES:", images)

        if product_form.is_valid():
            category_name = product_form.cleaned_data.get('category')
            category = None
            if category_name:
                category, _ = Category.objects.get_or_create(name=category_name)

            product = product_form.save(commit=False)
            product.category = category
            product.save()

            for img in images:
                ProductImage.objects.create(product=product, image=img)

            return redirect('product_list')
        else:
            print("Product form errors:", product_form.errors)

    else:
        product_form = ProductForm()
        image_form = MultiImageForm()

    return render(request, 'products/add_product.html', {
        'product_form': product_form,
        'image_form': image_form,
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


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})


def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'products/products_by_category.html', {'category': category, 'products': products})
