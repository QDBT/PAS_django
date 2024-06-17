from django.shortcuts import render,get_object_or_404,redirect
from homepage.models import Project
from .models import CodeSnippet
from django.contrib.auth.models import User
from .forms import CodeSnippetForm,CreateSnippetForm


def system_main(request,username,project_title):
    project = get_object_or_404(Project, title=project_title)
    snippets = CodeSnippet.objects.filter(project=project)
    
    if request.method == 'POST':
        ##Create a new snippet in a sidebar 
        if 'create_snippet' in request.POST:
            create_new_snippet_form =  CreateSnippetForm(request.post)
            if create_new_snippet_form.is_valid():
                new_snippet = create_new_snippet_form.save(commit=False)
                new_snippet.project = project
                 ##Check the title within project
                if  new_snippet.title and CodeSnippet.objects.filter(project=project,title=new_snippet.title).exists():
                    ## if already exit., add the error
                    create_new_snippet_form.add_error('title',f"The title '{new_snippet.title}' is already used")
                    ## send this to response because it wont be save
                    return render (request,'system_main/system_main.html',params)
                else:
                    new_snippet.title=project.title
                    new_snippet.save()
                    return redirect('main_system', username, project_title)
            
        ##Save the code after writting    
        elif 'writting_code_snippet' in request.POST:
            writting_code_snippet = CodeSnippetForm(request.post)
            if writting_code_snippet.is_valid():
                writting_code_snippet.save()
                return redirect('main_system', username, project_title)
    else:
        writting_code_snippet = CodeSnippetForm()
        create_new_snippet_form = CreateSnippetForm()
  
    ##send this data to HTML    
    params={
        'project': project,
        'writting_code_snippet':writting_code_snippet,
        'create_new_snippet_form':create_new_snippet_form,
        'snippets':snippets,
        'username':username
    }
    return render (request,'system_main/system_main.html',params)
