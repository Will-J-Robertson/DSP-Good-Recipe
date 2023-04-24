from django.urls import path
from .views import account, recipe, feedback

urlpatterns = [
    path('', account.admin_view, name="adminView"),
    path('/addRecipe', recipe.add_recipe, name="addRecipe"),
    path('/amendRecipe/<int:recipe_id>', recipe.amend_recipe, name="amendRecipe"),
    path('/deleteRecipe/<int:recipe_id>', recipe.delete_recipe, name="deleteRecipe"),
    path('/replyfeedback/<int:feedback_id>', feedback.replyfeedback, name="replyfeedback"),
    path('/deletefeedback/<int:feedback_id>', feedback.deletefeedback, name="deletefeedback"),
]