# homepage/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/', views.home_view, name='home'),
]