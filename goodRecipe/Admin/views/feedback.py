from django.shortcuts import render, redirect
from Customer.models import *
import smtplib
import ssl
from email.message import EmailMessage

#This function will send a reply to the base-user's email account
def replyfeedback(request, feedback_id):
    if feedback_id:
        # An object of the user's feedback is made
        feedback = Feedback.objects.get(id=feedback_id)

        # The email for that specific user is extracted from the object
        user_id = feedback.userID_id
        user = User.objects.get(id=user_id)
        user_email = user.username
        
        
    if request.POST:
        # Upon submittion the email reply is extracted.
        reply = request.POST['details']
        # The cooking recipe account's email and password are defined.
        email_sender = 'goodrecipe0@gmail.com'
        email_password = 'flqdinhdhlfzvpxd'

        # The the subject and body of the email are pre-set
        subject = 'Good Recipe >> Feedback Reply'
        body = """Dear Sir or Madam,

""" + reply + """

Yours Sincerly, 
GoodRecipe Management Team"""

        # The email function us called to send the reply 
        # from the admin to the base-user;s email address
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = user_email
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Login to the email and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, user_email, em.as_string())
        
        # The feedback is then removed from the database
        deletefeedback(request, feedback_id)
        return redirect('adminView')

    # The feedback of the user is returned to the html for the admin to survey.
    context = {
            "feedback":feedback,
        }
    return render(request, 'admin/viewFeedBack.html', context)
                      

# This function will take place when the feedback is 'removed'
def deletefeedback(request, feedback_id):
    if feedback_id:
        # The specific feedback is located and deleted from the database.
        feedback = Feedback.objects.get(id=feedback_id)
        feedback.delete()
    return redirect('adminView')