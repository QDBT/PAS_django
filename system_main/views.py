from django.shortcuts import render,get_object_or_404,redirect
from homepage.models import Project
from .models import CodeSnippet,CodeRecord
from django.contrib.auth.models import User
from .forms import CodeSnippetForm,CreateSnippetForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .runcode import run_code
import subprocess
import sys
import json

# Require username, project_title to connect to this views

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
                    return redirect('system_main', username, project_title)
            
        ##Save the code after writting    
        elif 'writting_code_snippet' in request.POST:
            writting_code_snippet = CodeSnippetForm(request.post)
            if writting_code_snippet.is_valid():
                writting_code_snippet.save()
                return redirect('system_main', username, project_title)
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

@require_POST
def save_snippet(request, username, project_title, snippet_id):
    snippet = get_object_or_404(CodeSnippet, id=snippet_id)

    # Get the Code from the frontend
    data = json.loads(request.body)

    # Update the Snippet for backend so it can show for the next time 
    snippet.code = data.get('code', '')
    snippet.save()

    # CodeRecord if it exists(if the code debuged before),
    if CodeRecord.objects.filter(CodeSnippet=snippet).exists():
        latest_code_record = CodeRecord.objects.filter(CodeSnippet=snippet).order_by('-created_at').first()
        
        #If the CodeRecord is exits ,checked the code is the same with the CodeRecord
        if latest_code_record and snippet.code == latest_code_record.original_code:

            #if the the code is the same, only show the lasted without create or debug anything
            output = latest_code_record.output
            error = latest_code_record.error
            print("the same with lastest")

        #if the code is different, create new record and debug it
        else:
            # Create a CodeRecord entry
            code_record = CodeRecord.objects.create(CodeSnippet=snippet, original_code=snippet.code)

            # Run the code and get the output and error
            output, error = run_code(snippet.code)
            code_record.output = output  # Store the output as fixed code for simplicity
            code_record.error = error
            code_record.save()

    #if the Code never debuged before, save and debug it    
    else:
        # Create a CodeRecord entry
        code_record = CodeRecord.objects.create(CodeSnippet=snippet, original_code=snippet.code)

        # Run the code and get the output and error
        output, error = run_code(snippet.code)
        code_record.output = output  # Store the output as fixed code for simplicity
        code_record.error = error
        code_record.save()
    # Return the output and error to the frontend
    return JsonResponse({'output': output, 'error': error})

