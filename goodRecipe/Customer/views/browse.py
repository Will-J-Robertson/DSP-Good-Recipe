from django.shortcuts import render, redirect
from Customer.models import *
from Customer.forms import *
from Customer.views.recommendation import *

# This function will return an object containing all the Recipes in the database
def get_recipes():
    all_recipes = Recipe.objects.all()
    return all_recipes

# This function will display all of the recipes in the database to the user.
# It will also display recipe favourites and both collabrative and content-based recommendations.
def recipe(request):
    all_recipes = get_recipes()
    collab_recommended_recipes = collaborative_filtering(request)
    content_recommended_recipes = content_based_filtering(request)
    favourite_recipes = []
    fav_num = 0

    # The recipe Ids that are returned from collabrative filtering are stored into an array
    collab_recipes_recommended = []
    for i in range (0, len(collab_recommended_recipes)):
        collab_recipes_recommended.append(Recipe.objects.get(id=collab_recommended_recipes[i]))
    # The recipe Ids that are returned from content-based filtering are stored into an array
    content_recipes_recommended = []
    for i in range (0, len(content_recommended_recipes)):
        content_recipes_recommended.append(Recipe.objects.get(id=content_recommended_recipes[i]))
    
    # All of the favourites from the database that belong to the user are placed into an object.
    fav = Favourites.objects.filter(userID_id=request.user.id)

    # The number of times the recipe is favourites is calculated
    for favs in fav:
        favourite_recipes.append(Recipe.objects.get(id=favs.recipeID_id))
        fav_num += 1

    # All favourited recipes, all recommended recipes and all the recipes in the database
    # are passed into the front end, being displayed to the user
    context= {
        'all_recipes': all_recipes,
        'collab_recommended': collab_recipes_recommended,
        'content_recommended': content_recipes_recommended,
        'favourites' : favourite_recipes,
        'fav_num' : fav_num,
    }
    # The recipe view html is displayed to the user
    return render(request, 'Customer/recipeView.html', context)


# This function is responsible for displaying the recipe details to the user
def recipeDetails(request, recipe_id):
    # The favourite and rating forms are defined
    favourites = FavouriteForm(request.POST)
    ratings = RatingsForm(request.POST)
    if recipe_id:        
        # The recipe and its details are placed into an object ready to be displayed
        recipe = Recipe.objects.get(id=recipe_id)
        # The tags from the recipe are appended to an array ready to be displayed
        tags = []
        for name, value in vars(Tags.objects.get(recipeID_id=recipe_id)).items():
            if name != 'id':
                if name != 'recipeID_id':
                    if value == 1:
                        tags.append(name)
    if request.POST:
        # If the user favourites the recipe:
        if 'favourite-1' in request.POST:
            if favourites.is_valid():
                # A favourite record is added to the 'Favourites' table
                # The recipe is now a favourite of the users
                favourite = favourites.save(commit=False)
                favourite.userID = request.user
                favourite.recipeID = Recipe.objects.get(id=recipe_id)
                favourite.save()
                # The total times the recipe is favourited is incremented
                total_fav = Recipe.objects.get(id=recipe_id)
                total_fav.numFavourited += 1
                total_fav.save()
                return redirect('details', recipe_id)
            else:
                return redirect('recipe')
            
        if 'form-1' in request.POST:
            # If the user gives a rating to the recipe:
            # A rating record is added to the table 'Ratings' with the userID, recipeID and rating
            if ratings.is_valid():
                # If the user has previously made a rating that rating is then updated with the new rating
                if Ratings.objects.filter(recipeID_id=recipe_id, userID_id=request.user).exists():
                    rate= Ratings.objects.get(recipeID_id=recipe_id, userID_id=request.user)
                    rate.rating = int(request.POST.get("form-1"))
                    rate.save()
                    return redirect('details', recipe_id)
                else:
                    # If this is the first time a rating is made, 
                    # the rating is added to the database
                    rating = ratings.save(commit=False)
                    rating.userID = request.user
                    rating.recipeID = Recipe.objects.get(id=recipe_id)
                    rating.rating = int(request.POST.get("form-1"))
                    rating.save()
                    return redirect('details', recipe_id)
            else:
                print('Your Rating forms is not correct :(')
                print(ratings.errors)
                return redirect('recipe')

    # Checks if the user has favourited the recipe, which will be passed to the front-end
    context = {"recipe":recipe,"userID":request.user,"recipeID":Recipe.objects.get(id=recipe_id),"tags":tags,'FavouriteForm': favourites,}
    if Favourites.objects.filter(recipeID_id=recipe_id, userID_id=request.user).exists():
        fav = Favourites.objects.get(recipeID_id=recipe_id, userID_id=request.user)
        context["fav"] = fav

    # Checks if the user has rated the recipe, which will be passed to the front-end
    if Ratings.objects.filter(recipeID_id=recipe_id, userID_id=request.user).exists():
        rates = Ratings.objects.get(recipeID_id=recipe_id, userID_id=request.user)
        context["RatingsForm"] = ratings
        context["rating"] = rates
    else:
        context["RatingsForm"] = ratings
    # The user will be transfered to the recipe details page
    return render(request, 'Customer/recipeDetails.html', context)

# This function will remove a recipe from the user's favourites.
def removeFavourite(request, recipe_id, user_id):
    if recipe_id:
        if user_id:
            # If the favourite record is found, it will then be removed from the table
            favouriteID = Favourites.objects.get(recipeID_id=recipe_id, userID_id=user_id)
            favouriteID.delete()
            # Once removed, the total number of favourites is decremented.
            total_fav = Recipe.objects.get(id=recipe_id)
            total_fav.numFavourited -= 1
            total_fav.save()

    return redirect('details', recipe_id)
