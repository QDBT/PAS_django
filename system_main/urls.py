from django.urls import path
from . import views

urlpatterns = [
    path('',views.system_main,name='system_main'),
    path('save_snippet/<int:snippet_id>/', views.save_snippet, name='save_snippet'),
    path('feedback/<int:snippet_id>/',views.feedback,name='feedback')
]
