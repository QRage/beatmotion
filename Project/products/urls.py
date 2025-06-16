from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.products_by_category, name='products_by_category'),
    path('compare/', views.product_comparison_view, name='product_compare'),
    path('compare/add/<int:product_id>/', views.add_to_comparison_view, name='add_to_comparison'),
    path('compare/remove/<int:product_id>/', views.remove_from_comparison_view, name='remove_from_comparison'),
]
