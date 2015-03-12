from django.core.mail import EmailMessage

#Constants
REG_EMAIL_SUB = "Bark! Registration Code"
REG_EMAIL_CONT = "Hello and welcome to Bark!\n\nJust to check you are a human, please enter the following code when prompted: "

WELC_EMAIL_SUB = "Welcome to Bark!"
WELC_EMAIL_CONT = "Welcome to Bark!\n\nYour account is now active and ready-to-use."

EMAIL_FOOT = "If you ever need any help, there's a nice hand help function at the top of every page!\nRegard, The Bark Team"



#Sends a verifiction email to the user
def sendRegEmail(user):
    email = EmailMessage(REG_EMAIL_SUB, REG_EMAIL_CONT + user.code + EMAIL_FOOT, to=[user.email])
    email.send()


#Sends a happy welcome email to the user after their account has been active!
def sendWelcomeEmail(user):
    email = EmailMessage(WELC_EMAIL_SUB, WELC_EMAIL_CONT + EMAIL_FOOT, to=[user.email])
    email.send()
