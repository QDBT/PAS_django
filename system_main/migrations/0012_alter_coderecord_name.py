# Generated by Django 4.2.2 on 2024-11-13 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_main', '0011_alter_coderecord_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coderecord',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
