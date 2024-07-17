from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from homepage.models import Project

class CodeSnippet(models.Model):
    project =models.ForeignKey(Project,on_delete=models.CASCADE, related_name='snippets')
    title =models.CharField(max_length=255,blank=True)
    code= models.TextField(blank=True)
     

        
    def __str__(self):
        return f'{self.title}.{self.project.language}'
        
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.project.title
        super().save(*args, **kwargs)


class CodeRecord(models.Model):
    CodeSnippet=models.ForeignKey(CodeSnippet,on_delete=models.CASCADE, related_name='code_record')
    original_code=models.TextField()
    output=models.TextField(null=True,blank=True)
    error=models.TextField(null=True,blank=True)
    feedback_without_code=models.TextField(null=True,blank=True)
    feedback_only_code=models.TextField(null=True,blank=True)
    feedback_all=models.TextField(null=True,blank=True)
    token_input=models.SmallIntegerField(default = 0)
    token_respawn=models.SmallIntegerField(default = 0)
    created_at=models.DateTimeField(auto_now_add=True)

    def tokens(self):
        return self.token_input + self.token_respawn
    
    def __str__(self):
        return f'Record for {self.CodeSnippet.title} at {self.created_at}'
# Import the signals module to connect the signals
# the signals that automatically create a first snippet when the project is created
import homepage.signals