from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from homepage.models import Project

class CodeBox(models.Model):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE)
    TextArea = models.CharField(max_length=255, null=True)