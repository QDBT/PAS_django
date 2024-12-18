from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from system_main.models import File
from homepage.models import Project

@receiver(post_save, sender=User)
def create_initial_file(sender, instance, created, **kwargs):
    if created:
        # Create a Project instance for the user if necessary
        project, project_created = Project.objects.get_or_create(
            user=instance,
            defaults={'title': 'TRAINING', 'language': 'py'}
        )
        # Create a File instance associated with the new Project
        File.objects.create(
            project=project,
            file_name='Hello.py',
            code='# Default Python code here'
        )
    
    