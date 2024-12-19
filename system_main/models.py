from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from homepage.models import Project
from django.db import migrations, models
import uuid


class File(models.Model):
    project =models.ForeignKey(Project,on_delete=models.CASCADE, related_name='snippets')
    file_name =models.CharField(max_length=255,blank=True)
    language = models.CharField(max_length=255, blank=True)  # Allow blank values
    code= models.TextField(blank=True)
    

        
    def __str__(self):
        return f'{self.project.user.username}: {self.file_name}'
        
    def save(self, *args, **kwargs):
        # If the language is blank, inherit it from the project
        if not self.language and self.project:
            self.language = self.project.language or 'unknown'

        # If the file_name is blank, inherit it from the project's title
        if not self.file_name and self.project:
            self.file_name = f'{self.project.title or "Untitled"}.{self.language}'

        # Truncate the file_name if it exceeds the maximum length
        max_length = self._meta.get_field('file_name').max_length
        if len(self.file_name) > max_length:
            self.file_name = self.file_name[:max_length]

        super().save(*args, **kwargs)


class DebugRecord(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='code_records')
    file = models.ManyToManyField(File, related_name='file')  # Allow multiple snippets
    main_file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True, related_name='main_file_debug_records')
    output = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       
        file_names = ", ".join([file.file_name for file in self.file.all()])
        return f'MainFile:{self.main_file}  with {file_names} (created_at: {self.created_at})'


class AskAIRecord(models.Model):
    #Information put into AI
    project = models.ForeignKey(Project, on_delete=models.CASCADE)   
    file = models.ManyToManyField(File, blank=True) # Allow multiple snippets
    system_message = models.TextField(null=True, blank=True)
    user_message = models.TextField(null=True, blank=True)
    
    #Information after run AI
    AI_answer = models.TextField(null=True, blank=True)
    token_input=models.SmallIntegerField(default = 0)
    token_respawn=models.SmallIntegerField(default = 0)
    token_total = models.SmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)


    def tokens(self):
        return self.token_input + self.token_respawn
    
    def __str__(self):
        return f'Record AI create at {self.created_at}'
# Import the signals module to connect the signals
# the signals that automatically create a first snippet when the project is created
import homepage.signals