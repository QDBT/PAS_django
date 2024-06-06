# homepage/urls.py

from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
     path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
]