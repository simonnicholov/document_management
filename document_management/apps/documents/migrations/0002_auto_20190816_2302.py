# Generated by Django 2.2.3 on 2019-08-16 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentlogs',
            old_name='document_name',
            new_name='document_subject',
        ),
    ]