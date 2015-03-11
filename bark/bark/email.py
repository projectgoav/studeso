from django.core.mail import EmailMessage

#Constants
REG_EMAIL_SUB = "Bark! Registration Code"
REG_EMAIL_CONT = "Hello and welcome to Bark!\n\nJust to check you are a human, please enter the following code when prompted: "

EMAIL_FOOT = "If you ever need any help, there's a nice hand help function at the top of every page!\nRegard, The Bark Team"



#Sends a verifiction email to the user
def sendRegEmail(user):
    email = EmailMessage(REG_EMAIL_SUB, REG_EMAIL_CONT + user.code, to=[user.email])
    email.send()
