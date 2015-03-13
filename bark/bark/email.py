from django.core.mail import EmailMessage

#Constants
WELC_EMAIL_SUB = "Welcome to Bark!"
WELC_EMAIL_CONT = "Welcome to Bark!\n\nYour account is now active and ready-to-use."

EMAIL_FOOT = "If you ever need any help, there's a nice hand help function at the top of every page!\nRegard, The Bark Team"

#Sends a happy welcome email to the user after their account has been active!
def sendWelcomeEmail(user):
    email = EmailMessage(WELC_EMAIL_SUB, WELC_EMAIL_CONT + EMAIL_FOOT, to=[user.email])
    email.send()
