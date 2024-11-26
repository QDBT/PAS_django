from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    LANGUAGE_CHOICES = [
        ('py', 'python'),
        ('c', 'c'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.user.username} (Last modified: {self.last_modified})'
    
    def save(self, *args, **kwargs):
        #Check if the same titled Project already exits
        if not self.id:  
            base_title = self.title
            counter = 1
            #set up the different title 1 if the same title project exits 
            while Project.objects.filter(title=self.title).exists():
                self.title = f"{base_title}({counter})"
                counter += 1
        super(Project, self).save(*args, **kwargs)
