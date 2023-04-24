from django.urls import path
from .views import account, browse, feedback

urlpatterns = [
    path('', account.login_user, name="login"),
    path('logout', account.logout_User, name='logout'),
    path('register', account.register, name="register"),
    path('recipeView', browse.recipe, name="recipe"),
    path('recipeDetails/<int:recipe_id>', browse.recipeDetails, name="details"),
    path('recipeDetails/removeFavourite/<int:recipe_id>/<int:user_id>', browse.removeFavourite, name="details"),
    path('feedback', feedback.feedback, name="feedback"),
    path('amendDetails', account.amendDetails, name="amend"),
]