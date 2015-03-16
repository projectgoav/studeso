from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.views import password_change
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from bark.forms import UserForm, UserProfileForm
from bark.email import sendWelcomeEmail, sendChangeEmail, sendResetEmail
from bark.models import UserReset, UserProfile

#View a list of people on the site
def users(request):
    return HttpResponse("Person 1<br>Person 2<br>Person 3<br>Person 4")

#View specific user profile
def view_user(request):
    return HttpResponse("Person 1<br><br>Sample information<br>Sample information<br>More sample information")

#Update User Profile
#MUST BE LOGGED IN
@login_required
def profileUpdate(request):

    if request.method == 'POST':
            bio_text = request.POST.get('bio_data')
            request.user.userprofile.bio = bio_text
            request.user.save()

            if 'profile_picture' in request.FILES:
                request.user.userprofile.profile_picture = request.FILES['profile_picture']
                request.user.userprofile.save()

            return render(request, 'auth/timeout-page.html', { 'TITLE' : "Profile Updated", 'MESSAGE' : "Your profile has been updated"})

    else:
        user = request.user
        tags = user.userprofile.followed_tags.all()
        context_dic = { 'BIO' : user.userprofile.bio, 'tags' : tags }
        return render(request, "auth/profile-form.html", context_dic)

#Update your current profile
#MUST BE LOGGED IN
def profile_update(request):
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
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()

            try:
                sendWelcomeEmail(user)
            except:
                print "Unable to send welcome email :("

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
    return render(request, 'auth/timeout-page.html', {'TITLE' : "Logout", 'MESSAGE' : "You've logged out."} )

#Password option menu, just to fill a url!
def passwordMenu(request):
    return HttpResponse("You can do password stuff here")

#Password change
@login_required
def passwordChange(request):
    # Try and change password
    context_dic = { }
    context_dic['errors'] = []

    #If Post, get the data we need from the User
    if request.method == 'POST':
        oldpass = request.POST.get('old_password')
        password = request.POST.get('new_password1')
        password2 = request.POST.get('new_password2')

        #CFor error checking
        if not request.user.check_password(oldpass):
            context_dic['errors'] += ["Your current password is incorrect"]
        if (not password or not password2):
            context_dic['errors'] += ["New passsword(s) can't be blank!"]
        if password != password2 :
            context_dic['errors'] += ["Your new passwords didn't match"]

        #If error was found....
        if len(context_dic['errors']) > 0:
            #Otherwise, we return the errors from the form
            return render(request, 'auth/password-change.html', context_dic)

        request.user.set_password(password)
        request.user.save()
        update_session_auth_hash(request, request.user) # REQUIRED TO KEEP USER LOGGED IN WHEN THEY CHANGE PASSWORD

        #Once all is complete, we try and send an email then let them know of change
        try:
            sendChangeEmail(request.user)
        except:
            print "Unable to send password change email :("
        return render(request, 'auth/timeout-page.html', {'TITLE' : 'Password Changed', 'MESSAGE' : "You've changed your passowrd"})
    else:
        #Show the change form if no details given
        return render(request, 'auth/password-change.html', {})

#Password Reset
def passwordReset(request):
    context_dic = { }
    context_dic['errors'] = []

    #If Post, get the data we need from the User
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        #Try and find a matching User in the Bark database
        try:
            user = User.objects.get(username=username)
        except:
            context_dic['errors'] += ["No User with that username found."]

        #Check their email against they one they have given
        user_email = user.email
        if user_email != email:
            context_dic['errors'] = "The email matching username was wrong."

        if len(context_dic['errors']> 0):
            return render(request, 'auth/password-reset.html', context_dic)

        #Give them a nice wee code then email it to them
        # TODO randomly give a code to users
        # TODO check for existing code and remove before giving a new one.
        u = UserReset.objects.get_or_create(username=username, code=123456)[0]

        try:
            sendResetEmail(user, u.code)
        except:
            #If a problem,print the code to the terminal
            print "ERROR sending reset request. The code is" + str(u.code)
        return redirect('/password-reset-do/')
    else:
        #Show the reset form
        return render(request, 'auth/password-reset.html', {})

def passwordResetCode(request):
    context_dic = { }
    context_dic['errors'] = []

    #If Post, get the data we need from the User
    if request.method == 'POST':
        usern = request.POST.get('username')
        code = request.POST.get('code')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        #Form Error checking
        #Try and find a matching User in the Bark database
        try:
            user = User.objects.get(username=usern)
        except:
            context_dic['errors'] += ["No User with that username found."]
            return render(request, 'auth/reset-code.html', context_dic)

        #Check they've been given a reset code
        try:
            userReset = UserReset.objects.get(username=usern)
        except:
            context_dic['errors'] += ["Given username has not requested a password reset."]

        if not new_password1 or not new_password2:
            context_dic['errors'] += ["New password(s) can't be blank"]
        if new_password1 != new_password2 and new_password1 != "" and new_password2 != "":
            context_dic['errors'] += ["New passwords didn't macth"]
        if int(code) != userReset.code:
            context_dic['errors'] = "Reset code was wrong"

        if len(context_dic['errors'] > 0):
            return render(request, 'auth/reset-code.html', context_dic)

        #Once the checking is done, actually carry out the reset for them.
        user.set_password(new_password1)
        user.save()

        #Remember and remove reset from database, as it's no longer needed
        userReset.delete()

        try:
            sendChangeEmail(user)
        except:
            print "Could not send Reset complete email to user"

        return render(request, 'auth/timeout-page.html',  {'TITLE' : "Password Reset Complete", 'MESSAGE' : "Your password has been reset."})
    else:

        #Show the reset form
        return render(request, 'auth/reset-code.html', {})
