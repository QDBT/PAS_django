from django.shortcuts import render,get_object_or_404,redirect
from homepage.models import Project
from .models import File,AskAIRecord,DebugRecord,AskAIRecord
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .self_library import run_code,compare_code,CanAskAI,debug_code_with_file
from .API_OpenAI import OpenAI_API
from django.utils.timezone import localtime
import subprocess
import sys
import json
from django.utils.dateformat import format

    
# Require username, project_title to connect to this views

def system_main(request,username,project_title):
    user=get_object_or_404(User, username=username)
    project = get_object_or_404(Project,user=user, title=project_title)
    snippets = File.objects.filter(project=project)

    ##send this data to HTML    
    params={
        'project': project,
        'snippets':snippets,
        'username':username
    }
    return render (request,'system_main/system_main.html',params)


def update_or_create_files(project, server_data):  
    
    #Updates existing files or creates new ones based on server data.

    files = File.objects.filter(project=project)
    updated_files = []

    for i, file_data in enumerate(server_data):
        if i < len(files):
            # Update existing file
            file = files[i]
            file.code = file_data.get('Code', file.code)
            file.file_name = file_data.get('FileName', file.file_name)
            print ('change file name:',file.file_name)
        else:
            # Create a new snippet
            file = File(
                project=project,
                file_name=file_data.get('FileName'),
                language=file_data.get('Language', ''),
                code=file_data.get('Code', '')
            )
        file.save()
        updated_files.append(file)

    return updated_files


@require_POST
def save(request, username, project_title):

    #Handles saving the project snippets.
    
    user=get_object_or_404(User, username=username)
    project = get_object_or_404(Project,user=user, title=project_title)

    data = json.loads(request.body)
    front_data = data.get('FileData')

    update_or_create_files(project, front_data)
    return HttpResponse(status=204) #No content

def delete_file(request,username,project_title):
    user=get_object_or_404(User, username=username)
    project = get_object_or_404(Project,user=user, title=project_title)

    data = json.loads(request.body)
    front_file = data.get('file')
    file=get_object_or_404(File,project=project, file_name =front_file['FileName'])
    if file:
        file.delete()

    return HttpResponse(status=204) #No content

@require_POST
def code_debug(request, username, project_title):
    user=get_object_or_404(User, username=username)
    project = get_object_or_404(Project,user=user, title=project_title)

    # Get the Code from the frontend
    data = json.loads(request.body)
    server_data = data.get('FileData')

    
    # Update the Snippet for backend so it can show for the next time 
    updated_files =update_or_create_files(project, server_data)

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
    debug_record.file.set(updated_files)  # Associate snippets with the DebugRecord

    # Associate snippets with the DebugRecord
    debug_record.file.set(updated_files)  # Assuming `file` is a ManyToManyField in DebugRecord

    # Add the main_file to know which is debugged
    main_file = File.objects.get(file_name=main_file['FileName'], project=project)
    debug_record.main_file = main_file
    debug_record.save()

    # Return the output or error to the frontend
    return JsonResponse({'output': output, 'error': error, 'created_at':debug_record.created_at})

def feedback(request, username, project_title):
    user=get_object_or_404(User, username=username)
    project = get_object_or_404(Project,user=user, title=project_title)

    data = json.loads(request.body)
    created_at = data.get('created_at')
    frontend_user_message = data.get('UserMessage')
    if created_at is not None:
        ask_target=DebugRecord.objects.get(project=project, created_at=created_at)
    else:
        ask_target=None
    
    output=None
    diff = None

    give_to_API=[]
    user_message=[]

    if ask_target is not None:     
        #update all file
        for file in ask_target.file.all():
            if file.file_name != "Introduction":
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

    if frontend_user_message is not None:
        last_AI_record=AskAIRecord.objects.filter(project=project)
        print("lastar",last_AI_record)
        if last_AI_record.exists():
            last_AI_record=last_AI_record.order_by('created_at').last()
            print("last_AI_record",last_AI_record)
            user_message.append(last_AI_record.AI_answer)
        user_message.append(frontend_user_message)

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
    )
    if ask_target is not None:
        if ask_target.file:
            askAI_record.file.set(ask_target.file.all())
            askAI_record.save()            
    #Save it to send frontend next time if the feedback is the same
    #print(diff)
    
    
    return JsonResponse({'output':output, 'diff':diff})

    #This would happen if (debug the same code or had used all of first time feedback_option in the same code)
    
