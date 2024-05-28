from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login-signup/')
def home_view(request, username):
    user = get_object_or_404(User, username=username  )
    return render(request, 'homepage/home.html', {'user': user})