from django.shortcuts import render,get_object_or_404,redirect
from homepage.models import Project
from .models import CodeSnippet,CodeRecord
from django.contrib.auth.models import User
from .forms import CodeSnippetForm,CreateSnippetForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .self_library import run_code,IsSameCode,compare_code,CanAskAI
from .API_OpenAI import OpenAI_API
import subprocess
import sys
import json

## This is a global variable

#CanAskAI is the variable to setup permission to ask AI (run OpenAI_API())
#CanAskAI and it's options will be actived after debug the different code, and deactive after used all of that options
    
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

    # Compare the instant code and the lastest Code Record
    if IsSameCode(snippet):
        latest_code_record = CodeRecord.objects.filter(CodeSnippet=snippet).order_by('-created_at').first()
        output = latest_code_record.output
        error = latest_code_record.error
    
    #if the code is different ,or if this is the first code, create new record and debug it
    else:
        # Create a CodeRecord entry
        code_record = CodeRecord.objects.create(CodeSnippet=snippet, original_code=snippet.code)

        # Run the code and get the output and error
        output, error = run_code(snippet.code)
        code_record.output = output  # Store the output as fixed code for simplicity
        code_record.error = error
        code_record.save()
        print("code_record.save successful")




    # Return the output or error to the frontend
    return JsonResponse({'output': output, 'error': error})

def feedback(request,username,project_title,snippet_id):
    
    snippet = get_object_or_404(CodeSnippet, id=snippet_id)
    lastest_code_record = CodeRecord.objects.filter(CodeSnippet=snippet).order_by('-created_at').first()
    feedback_only_code = lastest_code_record.feedback_only_code
    feedback_without_code = lastest_code_record.feedback_without_code 
    data = json.loads(request.body)
    feedback_option = data.get('feedback_option')
    output=None
    diff = None

    #CanAskAI is the permission to run the API
    #CanAskAI always actives and only deactives when both options (without_code and only_code) are choosen before
    #It is for block multiple same feedback if the originalCode is unchanged or the same option
    #So it can reduced input token
    if CanAskAI(feedback_only_code,feedback_without_code,feedback_option):
        #Send to system what should it respawn depend feedback_option(without_code or only_code)
        system_message=f"Fixed it and show me {feedback_option}"
        if feedback_option =="only_code":
            system_message = system_message.__add__(" and don't put```")
        #init what we send to API
        content=[]

        #lastest_code_record had been saved after debuged, send that to API depend the debug was success or error
        if lastest_code_record.output:
            content.append(lastest_code_record.output)
        if lastest_code_record.error:
            content.append(lastest_code_record.error)
        #Also send all of the orginal_code to API
        content.extend(lastest_code_record.original_code)
        #Reduce the space of code for reduce input token
        content_string = "".join(content)

        output=None
        print(f"before API{lastest_code_record.feedback_only_code}")
        #Run OpenAI_API
        API_respawn = OpenAI_API(content_string,system_message)

        lastest_code_record.token_input += API_respawn[1]
        lastest_code_record.token_respawn += API_respawn[2]
        #Check the feedback_option and the permission to ask AI

        if feedback_option =="without_code":

            #The variable that returned from API will be input to the lastest_code_record
            feedback_without_code=API_respawn[0]
            output = feedback_without_code


            
        elif feedback_option =="only_code":
        
            #The variable that returned from API will be input to the lastest_code_record
            feedback_only_code = API_respawn[0]
            output = feedback_only_code

            diff = compare_code(lastest_code_record.original_code,feedback_only_code)

        #Save it to send frontend next time if the feedback is the same
        print(diff)
        lastest_code_record.save()
        return JsonResponse({'output':output, 'diff':diff})
    
    #This would happen if (debug the same code or had used all of first time feedback_option in the same code)
    else:
        print(f"Block Feedback because had used {feedback_option}")
        if feedback_option =="without_code":
            output = feedback_without_code
        elif feedback_option =="only_code":
            output = feedback_only_code
            diff = compare_code(lastest_code_record.original_code,feedback_only_code)
        return JsonResponse({'output':output, 'diff':diff})

