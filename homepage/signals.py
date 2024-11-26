from django.db.models.signals import post_save
from django.dispatch import receiver
from homepage.models import Project
from system_main.models import CodeSnippet

#Automatically create first CodeSnippet when the project Created
@receiver(post_save, sender=Project)
def create_first_snippet(sender, instance, created, **kwargs):
    if created and not CodeSnippet.objects.filter(project=instance).exists():
        CodeSnippet.objects.create(project=instance, file_name=f'{instance.title}.{instance.language}', code='')