from django.shortcuts import render, get_object_or_404,redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project
from .forms import ProjectForm

@login_required(login_url='/accounts/login-signup/')
def home(request,username):
    username1=get_object_or_404(User, username=username)
    projects = Project.objects.all()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('home', username=request.user.username)
    else:
        form = ProjectForm()
    params={
        'projects': projects,
        'username':username1,
        'form': form,
    }
    return render(request, 'homepage/home.html',params)
