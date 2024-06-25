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
    
    def language(self):
        if self.title.endswith('.py'):
            return ('python')
        elif self.title.endswith('.c'):
            return ('c')
        else:
            return self.project.language
        
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.project.title
        super().save(*args, **kwargs)


class CodeRecord(models.Model):
    CodeSnippet=models.ForeignKey(CodeSnippet,on_delete=models.CASCADE, related_name='code_record')
    original_code=models.TextField()
    fixed_code=models.TextField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Record for {self.CodeSnippet.title} at {self.created_at}'
# Import the signals module to connect the signals
# the signals that automatically create a first snippet when the project is created
import homepage.signals