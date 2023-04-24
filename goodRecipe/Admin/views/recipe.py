from django.shortcuts import render, redirect
from Customer.models import *
from Admin.forms import RecipeForm, TagForm

# This function will add a recipe to the database
def add_recipe(request):
    recipeForm = RecipeForm(request.POST, request.FILES)
    tagForm = TagForm(request.POST)
    if request.POST:
        # Upon the front-end being submitted, the user's input are 
        # validated in a validation check
        if recipeForm.is_valid():
            if tagForm.is_valid():
                # If the recipe passes all the validation checks
                # The recipe and tags are added to the database
                recipe = recipeForm.save()
                tags = tagForm.save(commit=False)
                # The tags are then connected to the recipe as a Foriegn key within the database
                tags.recipeID_id = recipe.id
                tags.save()

                return redirect('adminView')
            else:
                print('Your tags forms is not correct')
                print(recipeForm.errors) # If fails validation check then errors printed
                return redirect('addRecipe')
        else:
            print('Your recipe forms is not correct')
            print(recipeForm.errors)  # If fails validation check then errors printed
            return redirect('addRecipe')
    
    # The forms of the add recipe page are passed to the 
    # html to be retreive into the backend.
    context = {
        'recipeForm': recipeForm,
        'tagForm': tagForm,
    }
        
    return render(request, 'Admin/addRecipe.html', context)




# This function will amend a recipe in the database
def amend_recipe(request, recipe_id):
    if recipe_id:
        # The recipe and its tags are located in the database and made into an object.
        recipe = Recipe.objects.get(id=recipe_id)
        tag = Tags.objects.get(recipeID_id=recipe_id)
        if recipe:
            # The forms for the two objects are created and passed into the Html file for user input.
            editRecipeForm = RecipeForm(request.POST or None,request.FILES or None, instance=recipe)
            editTagForm = TagForm(request.POST or None, instance=tag)
            # Upon the front-end being submitted, the user's input are 
            # validated in a validation check
            if editRecipeForm.is_valid():
                if editTagForm.is_valid():
                    # The user's input is saved to the database
                    editRecipeForm.save()
                    editTagForm.save()
                    return redirect('adminView')

            # The recipe, tags and forms are passed into the html
            context = {
                "recipe":recipe,
                "tag": tag,
                "recipeForm": editRecipeForm,
                "tagForm": editTagForm,
            }
            return render(request, 'Admin/amendRecipe.html', context)
    

    return render(request, 'Admin/amendRecipe.html', context)


# This function will delete a recipe from the database.
def delete_recipe(request, recipe_id):
    if recipe_id:
        # If the recipe is found, delete the recipe and it's tags.
        lookup_recipe = Recipe.objects.get(id=recipe_id)
        tags = Tags.objects.get(recipeID_id=recipe_id)
        lookup_recipe.delete()
        tags.delete()
        # User is then re-directed to the admin view.
    return redirect('adminView')