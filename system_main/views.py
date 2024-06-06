from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import 

@login_required(login_url='/accounts/login-signup/')
def system_main(request,username,project_id)
    return render(request,'system_main.html')