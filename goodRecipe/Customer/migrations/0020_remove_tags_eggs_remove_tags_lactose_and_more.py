# Generated by Django 4.1.7 on 2023-04-12 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0019_tags_eggs_tags_lactose_tags_seasonal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='eggs',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='lactose',
        ),
        migrations.RemoveField(
            model_name='tags',
            name='seasonal',
        ),
    ]
