from django.shortcuts import render, redirect
from Customer.models import *
from Customer.forms import *

# This functionals purpose is to allow for the base-user 
# to send feedback to the administrators
def feedback(request):
    # The feedback form is passed to the html for user's input
    Feedback = FeedbackForm(request.POST)
    if request.POST:
        # Onces the form is submitted, its ran through a validation check
        if Feedback.is_valid():
            # If it passes, the feedback is stored to the database 
            # which the admin will be able to see
            FeedBack = Feedback.save(commit=False)
            FeedBack.userID = request.user
            FeedBack.save()
            return redirect('recipe')

        else:
            # If the user's input fails the validation check errors will print
            print('Your recipe forms is not correct')
            print(Feedback.errors)
            return redirect('feedback')
    
    # The feedback form is passed to the html for user's input
    context = {
        'FeedbackForm': Feedback,
    }
    return render(request, 'Customer/feedBack.html', context)
                      