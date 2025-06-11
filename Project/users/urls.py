from django.urls import path
from django.contrib.auth import views as auth_views

from .views import profile_view, register, LogoutGetView

app_name = 'users'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutGetView.as_view(), name='logout'),
]
