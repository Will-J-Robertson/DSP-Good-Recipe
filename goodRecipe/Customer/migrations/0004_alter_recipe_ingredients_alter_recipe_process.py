# Generated by Django 4.1.7 on 2023-04-08 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0003_alter_tags_easy_alter_tags_eggs_alter_tags_family_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='process',
            field=models.TextField(max_length=1000),
        ),
    ]
