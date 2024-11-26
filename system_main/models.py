from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from homepage.models import Project
from django.db import migrations, models
import uuid


class CodeSnippet(models.Model):
    project =models.ForeignKey(Project,on_delete=models.CASCADE, related_name='snippets')
    file_name =models.CharField(max_length=255,blank=True)
    language = models.CharField(max_length=255, blank=True)  # Allow blank values
    code= models.TextField(blank=True)
    

        
    def __str__(self):
        return f'{self.file_name}'
        
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


class CodeRecordAfterDebug(models.Model):
    CodeSnippet=models.ForeignKey(CodeSnippet,on_delete=models.CASCADE, related_name='code_record')    
    original_code=models.TextField()
    output=models.TextField(null=True,blank=True)
    error=models.TextField(null=True,blank=True)
    feedback_without_code=models.TextField(null=True,blank=True)
    feedback_only_code=models.TextField(null=True,blank=True)
    feedback_all=models.TextField(null=True,blank=True)
    token_input=models.SmallIntegerField(default = 0)
    token_respawn=models.SmallIntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)


    def tokens(self):
        return self.token_input + self.token_respawn
    
    def __str__(self):
        return f'Record for {self.CodeSnippet.file_name} at {self.created_at}'
# Import the signals module to connect the signals
# the signals that automatically create a first snippet when the project is created
import homepage.signals