from django.shortcuts import render,get_object_or_404,redirect
from homepage.models import Project
from .models import CodeSnippet,AskAIRecord,DebugRecord,AskAIRecord
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .self_library import run_code,IsSameCode,compare_code,CanAskAI,debug_code_with_file
from .API_OpenAI import OpenAI_API
from django.utils.timezone import localtime
import subprocess
import sys
import json
from django.utils.dateformat import format

## This is a global variable

#CanAskAI is the variable to setup permission to ask AI (run OpenAI_API())
#CanAskAI and it's options will be actived after debug the different code, and deactive after used all of that options
    
# Require username, project_title to connect to this views

def system_main(request,username,project_title):
    project = get_object_or_404(Project, title=project_title)
    snippets = CodeSnippet.objects.filter(project=project)

    ##send this data to HTML    
    params={
        'project': project,
        'snippets':snippets,
        'username':username
    }
    return render (request,'system_main/system_main.html',params)

@require_POST
def code_debug(request, username, project_title):
    project = get_object_or_404(Project, title=project_title)
    snippets = CodeSnippet.objects.filter(project=project)

    # Get the Code from the frontend
    data = json.loads(request.body)
    server_data = data.get('FileData')
    
    # Update the Snippet for backend so it can show for the next time 
    updated_snippets = []
    for i, frontend_data in enumerate(server_data):
        if i < len(snippets):
            # Update existing snippet
            snippet = snippets[i]
            snippet.code = frontend_data.get('Code', snippet.code)  # Update code if provided
            snippet.file_name = frontend_data.get('FileName', snippet.file_name)  # Update title if provided
        else:
            # Create a new snippet if the index exceeds the existing snippets
            snippet = CodeSnippet(
                project=project,
                file_name=frontend_data.get('FileName'),
                language=frontend_data.get('Language',''),
                code=frontend_data.get('Code', '')
            )
        snippet.save()
        updated_snippets.append(snippet)
        print('save',snippet)

    #Get Which is the File want to debug
    main_file = data.get('MainFileData')
    
    #Run debug 
    output, error = debug_code_with_file(server_data,main_file)
    
    #Create a DebugRecord
    debug_record = DebugRecord.objects.create(
        project=project,
        output=output,
        error=error,
    )
    #Change the timezone to same to frontend
    replace = localtime(debug_record.created_at).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    debug_record.created_at = replace

    # Associate snippets with the DebugRecord
    debug_record.file.set(updated_snippets)  # Assuming `file` is a ManyToManyField in DebugRecord
    # Add the main_file to know which is debugged
    main_snippet = CodeSnippet.objects.get(file_name=main_file['FileName'], project=project)
    debug_record.main_file = main_snippet
    
    debug_record.save()
    # Return the output or error to the frontend
    return JsonResponse({'output': output, 'error': error, 'created_at':debug_record.created_at})

def feedback(request, username, project_title):
    project = get_object_or_404(Project, title=project_title)

    data = json.loads(request.body)
    created_at = data.get('created_at')
    print(created_at)
    if created_at is not None:
        ask_target=DebugRecord.objects.get(project=project, created_at=created_at)
    output=None
    diff = None

    give_to_API=[]
    #CanAskAI is the permission to run the API
    #CanAskAI always actives and only deactives when both options (without_code and only_code) are choosen before
    #It is for block multiple same feedback if the originalCode is unchanged or the same option
    #So it can reduced input token
    if CanAskAI():
        #Send to system what should it respawn depend feedback_option(without_code or only_code)
        ##system_message=f"Fixed it and show me {feedback_option}"
        ##if feedback_option =="only_code":
            ##system_message = system_message.__add__(" and don't put```")
        #init what we send to API
        if ask_target is not None:
            user_message=[]
            #for file in ask_target.file.all():
                #filename=file.file_name
                #filecode=file.code
                #user_message.append({"FileName": filename, "Code": filecode})
            #lastest_code_record had been saved after debuged, send that to API depend the debug was success or error
            if ask_target.output:
                user_message.append(ask_target.output)
            if ask_target.error:
                user_message.append(ask_target.error)
            #Also send all of the orginal_code to API
            print(user_message)
            #Reduce the space of code for reduce input token
            content_string = "".join(user_message)

            output=None
            #Run OpenAI_API
            API_respawn = OpenAI_API(user_message)

            #lastest_code_record.token_input += API_respawn[1]
            #lastest_code_record.token_respawn += API_respawn[2]
            #Check the feedback_option and the permission to ask AI
            output =API_respawn[0]
            
            #Save it to send frontend next time if the feedback is the same
            #print(diff)
            
            
            return JsonResponse({'output':output, 'diff':diff})
    
    #This would happen if (debug the same code or had used all of first time feedback_option in the same code)
    
