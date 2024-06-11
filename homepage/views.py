from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Project
from .forms import ProjectForm


@login_required(login_url='/accounts/login-signup/')
def home(request,username):
    user=get_object_or_404(User, username=username)
    projects = Project.objects.filter(user=user)

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.start_at = timezone.now() 
            project.save()
            return redirect(f'/{username}/{project.title}/', {username,project.title})
    else:
        form = ProjectForm()
    params={
        'projects': projects,
        'username':user,
        'form': form,
    }
    return render(request, 'homepage/home.html',params)

def delete_project(request,username,project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return redirect('home',username)