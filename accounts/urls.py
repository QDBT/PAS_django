from django.urls import path
from . import views

urlpatterns =[
    path('login-signup/',views.login_signup_view, name='login_signup'),
    path('',views.login_signup_view, name='login_signup'),
]