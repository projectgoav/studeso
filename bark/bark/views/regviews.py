from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from bark.forms import UserForm, UserProfileForm
from bark.email import sendWelcomeEmail

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

#User can sign up. Once done, they'll get a nice welcome email :)
def signup(request):

    registered = False

    # If post, we want to sort out the form.
    if request.method == 'POST':
        #Get form data
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #Save form and password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            sendWelcomeEmail(user)

            registered = True

            #We re-direct home!
            # TODO Auto log in users here so they're all logged in and ready to roll.
            redirect('/')

        # If something went wrong, it goes to terminal and to the template.
        else:
            print user_form.errors, profile_form.errors

    # If GET, just display form
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'auth/signup.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


#User can sign in
def signin(request):
    # Try and login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Attempt to login
        user = authenticate(username=username, password=password)

        # If we've made it
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # TODO get some form of error page here.
                return HttpResponse("Your Bark account is disabled.")
        else:
            # TODO get some form of error page here.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        #Show the login form
        return render(request, 'auth/signin.html', {})


#User can sign out
@login_required
def signout(request):
    logout(request)
    return HttpResponseRedirect('/')

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
