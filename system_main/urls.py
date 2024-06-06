#systemmain/urls.py

from django.urls import path
from . import views

urlpatterns = [
     path('', views.system_main_view, name='system_main'),
     
]