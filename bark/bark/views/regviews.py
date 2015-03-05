from django.shortcuts import render
from django.http import HttpResponse

# Index Page
# Returns a welcome registration message
def index(request):
	return HttpResponse("Welcome to Bark!<br><br>Woof > Register!")


#View a list of people on the site
def users(request):
	return HttpResponse("Person 1<br>Person 2<br>Person 3<br>Person 4")

#View specific user profile
def viewuser(reequest):
	return HttpResponse("Person 1<br><br>Sample information<br>Sample information<br>More sample information")

#View the current user profile
#MUST BE LOGGED IN
def profile(request):
	return HttpResponse("You are person 1. Here is your information:<Br>Sample Info<br>Sample info<br>Sample info")

#Update your current profile
#MUST BE LOGGED IN
def profileUpdate(request):
	return HttpResponse("You wish to update your profile!?!?!?")



#User can sign up
def signup(request):
	return HttpResponse("You wish to join bark?!?!?")


#User can sign in
def signin(request):
	return HttpResponse("You wish to sign in!?!?!<br>You'll need to register first")

#User can sign out
def signout(request):
	return HttpResponse("Be off with you!")

#Password option menu, just to fill a url!
def passwordMenu(request):
	return HttpResponse("You can do password stuff here")

#Password change
#MUST BE LOGGED IN
def passwordChange(request):
	return HttpResponse("You can change you password")

#Password Reset
def passwordReset(request):
	return HttpResponse("You can reset you password. You twit. You much have forgotten it")

