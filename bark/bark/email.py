from django.core.mail import EmailMessage, send_mail
from bark.keys import USERNAME

#Constants
WELC_EMAIL_SUB = "Welcome to Bark!"
WELC_EMAIL_CONT = "Welcome to Bark!\n\nYour account is now active and ready-to-use."

CHANGE_EMAIL_SUB = "Bark Account : Password Change"
CHANGE_EMAIL_CONT1 = "Your Bark Account: "
CHANGE_EMAIL_CONT2 = " reccently changed your password. If this wasn't you, please contact the Bark Team!. If it was, please just ignore this email.\n\n"

RESET_EMAIL_SUB = "Bark Account : Password Reset"
RESET_EMAIL_CONT = "Your Bark account reset code: "

EMAIL_FOOT = "If you ever need any help, there's a nice hand help function at the top of every page!\nRegard, The Bark Team"

#Sends a happy welcome email to the user after their account has been active!
def sendWelcomeEmail(user):
    email = EmailMessage(WELC_EMAIL_SUB, WELC_EMAIL_CONT + EMAIL_FOOT, to=[user.email])
    email.send()

def sendChangeEmail(user):
    email = EmailMessage(CHANGE_EMAIL_SUB, CHANGE_EMAIL_CONT1 + user.username + CHANGE_EMAIL_CONT2 + EMAIL_FOOT, to=[user.email])
    email.send()

def sendResetEmail(email, code):
    email = EmailMessage(RESET_EMAIL_SUB, RESET_EMAIL_CONT + str(code), to=[email])
    email.send()
