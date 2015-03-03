from django.shortcuts import render
from django.http import HttpResponse

# Index Page
# Returns a welcome message
def index(request):
	return HttpResponse("Welcome to Bark!<br><br>Woof")

#Redirect index page
def Barkindex(request):
	return HttpResponse("Welcome to Bark!<br><br>Woof <br><br>We need to put a redirect here")


#Bark Tag listing
def barks(request):
	return HttpResponse("Random Bark 1<br>Random Bark 2<br>Random Bark 3<br>")

#View a specific bark
def barkview(request):
	return HttpResponse("Random Bark 1<br><br>Blah. Blah. Blah. Blah.<br><b>Author:</b>Blah.")


#Search view
def search(request):
	return HttpResponse("Perform a fantastic search!")




