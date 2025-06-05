from django.urls import path, include

from .views import home_view, LogoutGetView


urlpatterns = [
    path('', home_view, name='home'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', LogoutGetView.as_view(), name='logout'),
]
