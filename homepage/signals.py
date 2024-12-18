from django.db.models.signals import post_save
from django.dispatch import receiver
from homepage.models import Project
from system_main.models import File

#Automatically create first File when the project Created
@receiver(post_save, sender=Project)
def create_first_snippet(sender, instance, created, **kwargs):
    if created and not File.objects.filter(project=instance).exists():
        File.objects.create(project=instance, file_name=f'{instance.title}.{instance.language}', code='')

