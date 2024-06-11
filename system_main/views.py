from django.shortcuts import render

def system_main(request,username,project_title):
    return render (request,'system_main.html')
