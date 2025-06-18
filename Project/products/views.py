from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import ProductForm, MultiImageForm
from .models import ProductImage, Product, Category
from .comparison import add_to_comparison, remove_from_comparison

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
    product_list = Product.objects.all().order_by('-id')
    paginator = Paginator(product_list, 12)

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

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


def product_comparison_view(request):
    ids = request.session.get('comparison', [])
    products = Product.objects.filter(id__in=ids).prefetch_related('attributes__attribute')

    attribute_names = set()
    product_data = []

    for p in products:
        data = {}
        for val in p.attributes.all():
            data[val.attribute.name] = val.value
            attribute_names.add(val.attribute.name)
        product_data.append({'product': p, 'attributes': data})

    attribute_names = sorted(attribute_names)

    return render(request, 'products/compare.html', {
        'products': product_data,
        'attribute_names': attribute_names,
    })


def add_to_comparison_view(request, product_id):
    add_to_comparison(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))


def remove_from_comparison_view(request, product_id):
    remove_from_comparison(request, product_id)
    return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))
