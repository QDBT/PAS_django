# Generated by Django 4.2.2 on 2024-06-21 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0007_alter_project_language'),
        ('system_main', '0004_alter_codesnippet_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codesnippet',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to='homepage.project'),
        ),
        migrations.CreateModel(
            name='CodeRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_code', models.TextField()),
                ('fixed_code', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('CodeSnippet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_record', to='system_main.codesnippet')),
            ],
        ),
    ]
