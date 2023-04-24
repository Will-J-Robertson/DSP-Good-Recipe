# Generated by Django 4.1.7 on 2023-04-07 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipeName', models.CharField(default='Food Item', max_length=50)),
                ('shortDescription', models.CharField(default='Eat me', max_length=200)),
                ('PrepTime', models.CharField(default='30min', max_length=10)),
                ('calories', models.CharField(default='100Cal', max_length=3)),
                ('numFavourited', models.IntegerField(default=0)),
                ('ingredients', models.CharField(max_length=200)),
                ('process', models.CharField(max_length=200)),
                ('recipe_image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vegan', models.IntegerField(default=0)),
                ('vegetarian', models.IntegerField(default=0)),
                ('spicy', models.IntegerField(default=0)),
                ('lowCalorie', models.IntegerField(default=0)),
                ('highCalorie', models.IntegerField(default=0)),
                ('halal', models.IntegerField(default=0)),
                ('nuts', models.IntegerField(default=0)),
                ('fish', models.IntegerField(default=0)),
                ('lactose', models.IntegerField(default=0)),
                ('eggs', models.IntegerField(default=0)),
                ('wheat', models.IntegerField(default=0)),
                ('soya', models.IntegerField(default=0)),
                ('seasonal', models.IntegerField(default=0)),
                ('fast', models.IntegerField(default=0)),
                ('easy', models.IntegerField(default=0)),
                ('hard', models.IntegerField(default=0)),
                ('family', models.IntegerField(default=0)),
                ('partners', models.IntegerField(default=0)),
                ('single', models.IntegerField(default=0)),
                ('recipeID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Customer.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RegularUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, unique=True)),
                ('clearance', models.IntegerField(default=1)),
                ('classification', models.CharField(default='0', max_length=10)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipeID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Customer.recipe')),
                ('userID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
