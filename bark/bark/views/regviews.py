from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.views import password_change
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from bark.forms import *
from bark.email import sendWelcomeEmail, sendChangeEmail, sendResetEmail
from bark.models import UserReset, UserProfile

#View a list of people on the site
def users(request):
    return HttpResponse("Person 1<br>Person 2<br>Person 3<br>Person 4")

#View specific user profile
def view_user(request):
    return HttpResponse("Person 1<br><br>Sample information<br>Sample information<br>More sample information")

#Update User Profile with given data
#MUST BE LOGGED IN
@login_required
def profileUpdate(request):

    if request.method == 'POST':
        #Get form data
        form = UserProfileUpdateForm(data=request.POST)
        if form.is_valid():
            bio = form.cleaned_data['bio']

            #Check if they have a new Profile Image
            if 'profile_picture' in request.FILES:
                request.user.userprofile.profile_picture = request.FILES['profile_picture']
                request.user.userprofile.save()

            #Update their tag description with their about-me text
            request.user.userprofile.user_tag.description = bio
            request.user.userprofile.user_tag.save(update=True)

            return render(request, 'auth/timeout-page.html', { 'TITLE' : "Profile Updated", 'MESSAGE' : "Your profile has been updated"})
    else:

        form = UserProfileUpdateForm(request=request, initial={ 'bio' : request.user.userprofile.user_tag.description})

    return render(request, "auth/profile-form.html", {'profile_form' : form, 'img' :request.user.userprofile.profile_picture})

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
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()

            try:
                sendWelcomeEmail(user)
            except:
                print "Unable to send welcome email :("

            registered = True

            # Auto login the user to their new account!
            # MAKE SURE TO USE THE GIVEN USR AND PWD FROM POST
            if registered == True:
                nuser = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
                # If we've made it
                if nuser:
                    if nuser.is_active:
                        login(request, nuser)
                        return HttpResponseRedirect('/')
                else:
                    print "Something went wrong, logging in...."

        # If something went wrong, it goes to terminal and to the template.
        else:
            print user_form.errors, profile_form.errors

    # If GET, just display form
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'auth/signup.html', {'user_form': user_form, 'profile_form': profile_form} )


#User can sign in
def signin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Attempt to login
            user = authenticate(username=username, password=password)
            # If we've made it
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')

            else:
                print form.errors
        else:
            print form.errors

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'auth/signin.html', {'login_form': form})


#User can sign out
@login_required
def signout(request):
    logout(request)
    return render(request, 'auth/timeout-page.html', {'TITLE' : "Logout", 'MESSAGE' : "You've logged out."} )

#Password change
@login_required
def passwordChange(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordChangeForm(request.POST, request=request)
        # check whether it's valid:
        if form.is_valid():
            newpass = form.cleaned_data['new_pass1']

            request.user.set_password(newpass)
            request.user.save()
            update_session_auth_hash(request, request.user)

            try:
                sendChangeEmail(request.user)
            except:
                print "Unable to send password change email :("

            return render(request, 'auth/timeout-page.html', {'TITLE' : 'Password Changed', 'MESSAGE' : "You've changed your password"})
        else:
            print form.errors

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordChangeForm(request=request)

    return render(request, 'auth/password-change.html', {'change_form': form})

#Password Reset
def passwordReset(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordResetForm1(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            u = UserReset.objects.get_or_create(username=username, code=123456)[0]

            try:
                sendResetEmail(email, u.code)
            except:
                #If a problem,print the code to the terminal
                print "ERROR sending reset request. The code is" + str(u.code)
            return redirect('/password-reset-do/')

        else:
            print form.errors

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordResetForm1()

    return render(request, 'auth/password-reset.html', {'reset_form': form})

def passwordResetCode(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordResetForm2(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_pass1']

            user = User.objects.get(username=username)
            userReset = UserReset.objects.get(username=username)

            #Once the checking is done, actually carry out the reset for them.
            user.set_password(new_password)
            user.save()

            #Remember and remove reset from database, as it's no longer needed
            userReset.delete()

            try:
                sendChangeEmail(user)
            except:
                print "Could not send Reset complete email to user"

            return render(request, 'auth/timeout-page.html',  {'TITLE' : "Password Reset Complete", 'MESSAGE' : "Your password has been reset."})

        else:
            print form.errors

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordResetForm2()

    return render(request, 'auth/reset-code.html', {'reset_form': form})
