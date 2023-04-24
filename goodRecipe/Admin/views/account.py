from django.shortcuts import render
from Customer.models import *

# This function will return an object containing all the Recipes in the database
def get_recipes(): 
    all_recipes = Recipe.objects.all()
    return all_recipes

# This function will return an object containing all the Feedback in the database
def get_feedback():
    all_feedback = Feedback.objects.all()
    return all_feedback

# This function will send the two objects to the admin View, 
# html form that will be displayed to the user.
def admin_view(request):
    all_recipes = get_recipes()
    all_feedback = get_feedback()

    context= {
        'all_recipes': all_recipes,
        'all_feedback': all_feedback,
    }
    return render(request, 'admin/adminView.html', context)