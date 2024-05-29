from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_at = models.DateTimeField()
    program_language = models.CharField(max_length=255)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} by {self.user.username} (Last modified: {self.last_modified})'