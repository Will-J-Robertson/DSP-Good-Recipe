from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from Customer.models import *

# Forms help the back-end and database connect to the front-end of the website

# The Usercreation form will request all of the user's data that was inputted in the front-end,
# once submitted the values will be placed into the columns of the table 'User' specified by 'fields'
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password1', 'password2']

# The Register user form will request all of the user's data that was inputted in the front-end,
# once submitted the values will be placed into the columns of the table 'RegularUser' specified by 'fields'
class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = RegularUser
        fields = ['phone']

# The favourite form will request the two IDs of the user and the recipe to connect them in the favourite database
# the values will be stored in the columns of the table 'Favourites'.
class FavouriteForm(forms.ModelForm):
    class Meta:
        model = Favourites
        fields = ['userID', 'recipeID']

# The Feedback form will request all of the feedback details including the variables specified in 'fields',
# once the feedback is submitted the values will be stored into the database in the respective columns
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['userID','rating', 'details', 'anonymous']

# The ratings form will request the two IDs of the user and recipe along with the rating these values
# will be stored in the respective columns in the table 'Ratings', connecting a user to a recipe with a rating.
class RatingsForm(forms.ModelForm):
    class Meta:
        model = Ratings
        fields = ['userID','recipeID', 'rating']
