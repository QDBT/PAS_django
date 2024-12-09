from django.shortcuts import render,get_object_or_404,redirect
from homepage.models import Project
from .models import CodeSnippet,AskAIRecord,DebugRecord,AskAIRecord
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse,HttpResponse
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

def update_or_create_snippets(project, server_data):  
    
    #Updates existing snippets or creates new ones based on server data.

    snippets = CodeSnippet.objects.filter(project=project)
    updated_snippets = []

    for i, snippet_data in enumerate(server_data):
        if i < len(snippets):
            # Update existing snippet
            snippet = snippets[i]
            snippet.code = snippet_data.get('Code', snippet.code)
            snippet.file_name = snippet_data.get('FileName', snippet.file_name)
        else:
            # Create a new snippet
            snippet = CodeSnippet(
                project=project,
                file_name=snippet_data.get('FileName'),
                language=snippet_data.get('Language', ''),
                code=snippet_data.get('Code', '')
            )
        snippet.save()
        updated_snippets.append(snippet)

    return updated_snippets


@require_POST
def save(request, username, project_title):

    #Handles saving the project snippets.
    
    project = get_object_or_404(Project, title=project_title)
    data = json.loads(request.body)

    update_or_create_snippets(project, data)
    return HttpResponse(status=204) #No content



@require_POST
def code_debug(request, username, project_title):
    project = get_object_or_404(Project, title=project_title)

    # Get the Code from the frontend
    data = json.loads(request.body)
    server_data = data.get('FileData')
    
    # Update the Snippet for backend so it can show for the next time 
    updated_snippets = update_or_create_snippets(project, server_data)

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
     # Format the created_at timestamp
    debug_record.created_at = localtime(debug_record.created_at).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    debug_record.file.set(updated_snippets)  # Associate snippets with the DebugRecord

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
            #update all file
            for file in ask_target.file.all():
                filename=file.file_name
                filecode=file.code
                user_message.append(f"file_name: {filename}, code: {filecode}")

            #append to API know which was debug
            if ask_target.main_file:
                user_message.append(f"This file was debug:{ask_target.main_file}")
                
            #lastest_code_record had been saved after debuged, send that to API depend the debug was success or error
            if ask_target.output:
                user_message.append(ask_target.output)
            if ask_target.error:
                user_message.append(ask_target.error)
            
            output=None

            #Give to API
            give_to_API = {
                "user_message": user_message,

            }
            #Run OpenAI_API
            API_respawn = OpenAI_API(give_to_API)

            #lastest_code_record.token_input += API_respawn[1]
            #lastest_code_record.token_respawn += API_respawn[2]
            #Check the feedback_option and the permission to ask AI
            output =API_respawn["AI_answer"]
            
            askAI_record = AskAIRecord.objects.create(
                project=project,
                user_message=user_message,
                token_input=API_respawn["token_input"],
                token_respawn=API_respawn["token_respawn"],
                AI_answer=output,
                created_at=ask_target.created_at,
            )
            if ask_target.file:
                askAI_record.file.set(ask_target.file.all())
                askAI_record.save()            
            #Save it to send frontend next time if the feedback is the same
            #print(diff)
            
            
            return JsonResponse({'output':output, 'diff':diff})
    
    #This would happen if (debug the same code or had used all of first time feedback_option in the same code)
    
