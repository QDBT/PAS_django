from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from homepage.models import Project

class CodeSnippet(models.Model):
    project =models.ForeignKey(Project,on_delete=models.CASCADE)
    title =models.CharField(max_length=255,blank=True)
    code= models.TextField()
    
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