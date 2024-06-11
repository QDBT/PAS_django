from django.urls import path
from . import views

urlpatterns = [
    path('',views.system_main,name='system_main'),
]
