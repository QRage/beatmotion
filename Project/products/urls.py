from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('', views.product_list, name='product_list'),
]
