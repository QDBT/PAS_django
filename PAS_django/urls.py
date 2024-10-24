from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('',include('accounts.urls')),
    path('home/',include('homepage.urls')),
    path('<str:username>/', include('homepage.urls')),
    path('<str:username>/<str:project_title>/',include('system_main.urls')),
]
