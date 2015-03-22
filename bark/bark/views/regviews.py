from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.views import password_change
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from bark.forms import *
from bark.email import sendWelcomeEmail, sendChangeEmail, sendResetEmail
from bark.models import UserReset, UserProfile

import random, string

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
    context_dic = { }
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

    context_dic['form'] = form
    context_dic['page_head'] = "Update Profile"
    context_dic['help_text_2'] = """This is some of the personal information we've got about you.<br>You're welcome to change anything at any time!<br><br><b>Your 'About Me' appears when users click on your name tag. It's a post always at the top of the page, showing you off in all your glory!</b>"""
    context_dic['help_text_3'] = """Your current Profile Image is: <img src=" """ + request.user.userprofile.profile_picture.url + """ "width="32px" height="32px"  alt="Profile Image"/>"""
    context_dic['form_button'] = "Update your Profile"
    context_dic['form_url'] = "profile"
    context_dic['help_url'] = "json/profile_form.json"

    return render(request, 'auth/form.html', context_dic)

#User can sign up. Once done, they'll get a nice welcome email :)
def signup(request):
    context_dic = { }
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

    context_dic['form'] = user_form
    context_dic['form2'] = profile_form
    context_dic['page_head'] = "Sign Up"
    context_dic['help_text_2'] = """Sign up to Bark here to enjoy the full range of features Bark has to offer.<br>You aren't required to upload a profile image, but it might be nice to let others who you really are.<br><b>Don't worry if you forget, you can always update it later!</b>"""
    context_dic['help_text_3'] = """Already have an account? Sign in <a href="/signin/">here</a>"""
    context_dic['form_button'] = "Sign Up"
    context_dic['form_url'] = "signup"
    context_dic['help_url'] = "json/signup.json"

    return render(request, 'auth/form.html', context_dic)

#User can sign in
def signin(request):

    next_url = ""

    if request.GET:
        next_url = request.GET['next']

    context_dic = { }
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Attempt to login
            user = authenticate(username = username, password = password)
            # If we've made it
            if user:
                if user.is_active:
                    login(request, user)

                    if next_url == "":
                        return HttpResponseRedirect('/')
                    else:
                        return HttpResponseRedirect(next_url)

            else:
                print form.errors
        else:
            print form.errors

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    context_dic['form'] = form
    context_dic['next'] = next_url
    context_dic['page_head'] = "Sign In"
    context_dic['help_text_2'] = """Sign in to Bark!<br><b>Don't have an account?</b> <a href="/signin/">Sign up here!</a>"""
    context_dic['help_text_3'] = """Forgot your password? Reset it <a href="/password-reset-do/">here</a>"""
    context_dic['form_button'] = "Sign In"
    context_dic['form_url'] = "signin"
    context_dic['help_url'] = "json/signin.json"

    return render(request, 'auth/form.html', context_dic)


#User can sign out
@login_required
def signout(request):
    logout(request)
    return render(request, 'auth/timeout-page.html', {'TITLE' : "Logout", 'MESSAGE' : "You've logged out."} )

#Password change
@login_required
def passwordChange(request):
    context_dic = { }
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

    context_dic['form'] = form
    context_dic['page_head'] = "Change your Password"
    context_dic['form_button'] = "Change Password"
    context_dic['form_url'] = "passwordChange"
    context_dic['help_url'] = "json/change.json"

    return render(request, 'auth/form.html', context_dic)

#Password Reset
def passwordReset(request):
    context_dic = { }
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordResetForm1(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            randomCode = ""
            for i in range(0, random.randint(5, 10)):
                randomCode += str(random.choice(string.digits))

            u = UserReset.objects.get_or_create(username=username, code = randomCode)[0]

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

    context_dic['form'] = form
    context_dic['page_head'] = "Reset your Password"
    context_dic['help_text_2'] = """To reset your password enter your account username and the email it was registered with<br>You'll be emailed a <b>reset code</b> which will allow you to reset you password!"""
    context_dic['help_text_3'] = """Already got a code? <a href="/password-reset-do">Click here</a>"""
    context_dic['form_button'] = "Send Reset Code"
    context_dic['form_url'] = "passwordReset"
    context_dic['help_url'] = "json/passwordReset.json"

    return render(request, 'auth/form.html', context_dic)

def passwordResetCode(request):
    context_dic = { }
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

    context_dic['form'] = form
    context_dic['page_head'] = "Reset your Password"
    context_dic['help_text_2'] = """You should have recieved your reset code via email. If not <a href="/password-reset/">Click here to request another</a><br>Please re-enter your username, reset code and your new password to reset it!<br>Once you've reset your password, you'll need to login with your new details!"""
    context_dic['form_button'] = "Reset Password"
    context_dic['form_url'] = "passwordResetCode"
    context_dic['help_url'] = "json/resetCode.json"

    return render(request, 'auth/form.html', context_dic)
