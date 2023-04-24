from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from Customer.forms import *
from django.contrib.auth import login, authenticate,logout #Import for the authenticate feature for login and logout
from django.contrib.auth.decorators import login_required #Blocks function based on whether the user is logged in
from django.contrib.auth.models import Group #Import groups for user types

# This function authenticates the user's input with data in the database
# If the user's input is in the database then the user is logged into their account
def login_user(request):
    # A check is made incase the user is already logged in
    if request.user.is_anonymous==False:
        group = request.user.groups.all()[0].name
        if "Admin" in group:
            # If the user is an admin they are taken to the admin view
            return redirect('/recipeAdmin')
        else:
            # If the user is not an admin they are taken to the admin view
            return redirect('/recipeView')

    if request.method =="POST":
        # After the from is submitted the username (email) and password 
        # are passed into the pre-set django authenticate function
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        user=authenticate(request,username=email,password=password)

        # If the user is presenet in the database the user is transfered to the
        # admin view if admin, if a base-user they are transfered to the recipe view.
        if user is not None:
            login(request,user)
            group = request.user.groups.all()[0].name
            if "Admin" in group:
                return redirect('/recipeAdmin')
            else:
                return redirect('/recipeView')
        else:
            # If the user is not found in the database then an error message will be printed.
            error_message= "Invalid user not recognised"
            context = {
                "error_message":error_message
            }
            return render(request, 'Customer/login.html', context)
    else:
        # The user is displayed with the login html.
        return render(request, 'Customer/login.html')
                      
# This function allows for an user account to be added to the database
# If the user's input passes all of the validation checks then the account is created.
def register(request):

    # The two forms for user creation are made. user-form to handle authentication 
    # and the other, regular user form is used to store the user's details
    user_form = CreateUserForm()
    regular_user_form = RegisterUserForm()
    if request.method == 'POST':
        # Once the forms have been submitted the inputs are put through a validation check.
        user_form = CreateUserForm(request.POST)
        regular_user_form = RegisterUserForm(request.POST)
        if user_form.is_valid():
            if regular_user_form.is_valid():
                # If the validation is sucessful then the user is added to the database
                user = user_form.save()
                user=user_form.save()
                customer = regular_user_form.save(commit=False)
                customer.user = user
                customer.save()
                # The new user is given the user type 'Customer'
                group = Group.objects.get(name='Customer')
                user.groups.add(group)
                return redirect(login_user)
            else:
                # If the user fails the validation check then errors are presented.
                print("Not valid")
                print(regular_user_form.errors)
        else:
            # If the user fails the validation check then errors are presented.
            print("Not valid")
            print(user_form.errors)

    # User is presented with the register page html.
    return render(request, 
                  'Customer/register.html', 
                  {'user_form': user_form,'regular_user_form':regular_user_form}
                  )

# This function allows for a user's data to be amended in the database.
def amendDetails(request):
    user_id = request.user.id
    if user_id:
        # The user's data is located within the database and stored as temporary objects.
        customer = User.objects.get(id=user_id)
        phone = RegularUser.objects.get(user_id=user_id)
        if customer:
            # The two forms that will recieve the user's input are made
            editUserForm = CreateUserForm(request.POST or None,request.FILES or None, instance=customer)
            editUserForm2 = RegisterUserForm(request.POST or None,request.FILES or None, instance=phone)
            
            # Once submitted if the data passes the validation checks the data is then stored in the database
            if editUserForm.is_valid():
                    editUserForm.save()
                    editUserForm2.save()
                    return redirect('recipe')

            # The customer details and the two forms are passed into the html to present to the suer.
            context = {
                "customer":customer,
                "userForm": editUserForm,
                "userForm2": editUserForm2,
            }
            return render(request, 'Customer/amendDetails.html', context)
    return render(request, 'Customer/amendDetails.html', context)


# This Function will log out the user 
# from their session.
@login_required
def logout_User(request):
    logout(request)
    return redirect(login_user)