# Generated by Django 4.1.7 on 2023-04-08 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0006_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='userEmail',
            new_name='userID',
        ),
    ]