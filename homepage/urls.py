# homepage/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('homepage/',views.home_view, name='home'),
]