from django.shortcuts import render, get_object_or_404,redirect
from .models import Project, Assignment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login-signup/')
def home(request,username):
    projects = Project.objects.all()
    username = get_object_or_404(User, username=username  )
    params={
        'username': username,
        'projects': projects
    }
    return render(request, 'homepage/home.html',params)
