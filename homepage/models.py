from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    LANGUAGE_CHOICES = [
        ('Python', 'Python'),
        ('C', 'C'),
        ('HTML/CSS/JavaScript', 'HTML + CSS + JavaScript'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} by {self.user.username} (Last modified: {self.last_modified})'