from django.urls import path
from . import views

urlpatterns = [
    path('',views.system_main,name='system_main'),
    path('code_debug/', views.code_debug, name='code_debug'),
    path('feedback/',views.feedback,name='feedback')
]
