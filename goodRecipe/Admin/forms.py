from django import forms
from django.forms import ModelForm, Textarea
from Customer.models import *


# Forms help the back-end and database connect to the front-end of the website

# The recipe form will request all of the recipe details from the front-end,
# once submitted the values will be placed into the columns of the table 'Recipe' specified by 'fields'
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_image', 'recipeName','PrepTime', 'calories', 'shortDescription', 'ingredients', 'process']
        widgets = {
            'shortDescription': forms.Textarea(attrs={'rows': 6}),
            'ingredients': forms.Textarea(attrs={'rows': 10}),
            'process': forms.Textarea(attrs={'rows': 15}),
        }

# The tag form will request all of the tag boolean values from the front-end,
# once the recipe is submitted the boolean values will be placed into the columns of the table 'Tags' specified in 'fields'
class TagForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['vegan', 'vegetarian', 'spicy', 'lowCalorie', 'highCalorie', 'halal', 'nuts', 'fish', 'dairy', 'lactose', 
                  'egg', 'wheat', 'soya', 'slow', 'fast', 'easy', 'hard', 'family', 'partners', 'single']
