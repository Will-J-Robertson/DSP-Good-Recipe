# Generated by Django 4.1.7 on 2023-04-12 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0017_ratings'),
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
        migrations.AddField(
            model_name='tags',
            name='dairy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tags',
            name='egg',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tags',
            name='slow',
            field=models.BooleanField(default=False),
        ),
    ]