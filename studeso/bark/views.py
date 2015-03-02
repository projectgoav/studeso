from django.shortcuts import render
from django.http import HttpResponse

# Index Page
# Returns a welcome message
def index(request):
	return HttpResponse("Welcome to Bark!<br><br>Woof")