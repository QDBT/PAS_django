# Generated by Django 4.2.2 on 2024-05-30 06:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_alter_project_description_alter_project_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='program_language',
        ),
        migrations.AddField(
            model_name='project',
            name='language',
            field=models.CharField(choices=[('Python', 'Python'), ('C', 'C'), ('HTML/CSS/JavaScript', 'HTML + CSS + JavaScript')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='start_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
