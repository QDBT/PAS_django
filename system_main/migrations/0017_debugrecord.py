# Generated by Django 4.2.2 on 2024-12-03 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_alter_project_language'),
        ('system_main', '0016_rename_title_codesnippet_file_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebugRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('output', models.TextField(blank=True, null=True)),
                ('error', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.ManyToManyField(related_name='file', to='system_main.codesnippet')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_records', to='homepage.project')),
            ],
        ),
    ]
