from django.urls import path

from . import views


app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
]
