# Generated by Django 4.2.2 on 2024-12-10 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_alter_project_language'),
        ('system_main', '0021_rename_formatted_created_at_debugrecord_created_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CodeSnippet',
            new_name='File',
        ),
    ]