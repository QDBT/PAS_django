from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login-signup/')
def home_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'homepage/home.html', {'user': user})