# Generated by Django 4.2.2 on 2024-11-22 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system_main', '0013_remove_coderecord_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CodeRecord',
            new_name='CodeRecordAfterDebug',
        ),
    ]
