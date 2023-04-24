from django.db import models
from django.contrib.auth.models import User

# The Models are used to create the tables within the database
# The column name, datatype and parmeters are specified for each variable

class Recipe(models.Model):
    recipeName = models.CharField(max_length=50, default = "Food Item")
    shortDescription = models.TextField(max_length=200, default = "Eat me")
    PrepTime = models.CharField(max_length=10, default = "30min")
    calories = models.CharField(max_length=3, default = "100Cal")
    numFavourited = models.IntegerField(default=0)
    ingredients = models.TextField(max_length=500)
    process = models.TextField(max_length=4000)
    recipe_image = models.ImageField(upload_to="images/")


class Tags(models.Model):
    recipeID = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
    vegan = models.BooleanField(default=False)
    vegetarian = models.BooleanField(default=False)
    spicy = models.BooleanField(default=False)
    lowCalorie = models.BooleanField(default=False)
    highCalorie = models.BooleanField(default=False)
    halal = models.BooleanField(default=False)
    nuts = models.BooleanField(default=False)
    fish = models.BooleanField(default=False)
    dairy = models.BooleanField(default=False)
    lactose = models.BooleanField(default=False)
    egg = models.BooleanField(default=False)
    wheat = models.BooleanField(default=False)
    soya = models.BooleanField(default=False)
    slow = models.BooleanField(default=False)
    fast = models.BooleanField(default=False)
    easy = models.BooleanField(default=False)
    hard = models.BooleanField(default=False)
    family = models.BooleanField(default=False)
    partners = models.BooleanField(default=False)
    single = models.BooleanField(default=False)

class RegularUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone=models.CharField(max_length=11,unique=True, null=True, blank=True)

class Favourites(models.Model):
    userID = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    recipeID = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.CASCADE)

class Feedback(models.Model):
    userID = models.ForeignKey(User, blank = True, on_delete=models.CASCADE)
    feedbackRatings = (('highlySatisfied', 'Highly Satisfied'), ('Satisfied', 'Satisfied'), ('Moderate', 'Moderate'), ('CouldDoBetter', 'Could Do Better'), ('Unsatisfied', 'Unsatisfied'))
    rating = models.CharField(max_length=24, choices=feedbackRatings)
    details = models.TextField(max_length=2000)
    anonymous = models.BooleanField(default=False, blank=True)

class Ratings(models.Model):
    userID = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    recipeID = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)