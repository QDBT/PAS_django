# Generated by Django 4.2.2 on 2024-11-26 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0008_alter_project_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='language',
            field=models.CharField(choices=[('py', 'python'), ('c', 'c')], max_length=50),
        ),
    ]
