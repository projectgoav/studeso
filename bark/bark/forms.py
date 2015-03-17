from django import forms
from django.contrib.auth.models import User
from bark.models import UserProfile, Post, UserReset
from django.views.generic.edit import CreateView


# Get data for user when they sign up
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


# Get data for the User Profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture',)


class PostForm(forms.ModelForm):
    class Meta:
        # Provide an association between PostForm and Post.
        model = Post
        exclude = ('slug', 'views', 'author', 'creation_date', 'rating',)

        def form_valid(self, form):
            form.instance.author = self.request.user
            return super(Meta, self).form_valid(form)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(), required=True)

    def clean(self):

        #Checking the existance of the username and password
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                self.add_error('password', "Password invalid")
        except:
            self.add_error('username', "Invalid Username and Password")
            self.add_error('password', "Invalid Username and Password")
            return


class PasswordResetForm1(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    email = forms.EmailField(label='Account Email', max_length=50, required=True)

    def clean(self):
        cleaned_data = super(PasswordResetForm1, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        try:
            user = User.objects.get(username=username)
        except:
            self.add_error('username', 'No account with that Username found.')
            self.add_error('email','')
            return

        if user.email != email:
            self.add_error('email', 'Account email is incorrect.')


class PasswordResetForm2(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    code = forms.CharField(label='Reset Code', required=True)
    new_pass1 = forms.CharField(label='New Password', max_length=50, widget=forms.PasswordInput(), required=True)
    new_pass2 = forms.CharField(label='New Passowrd (Again)', max_length=50, widget=forms.PasswordInput(), required=True)


    def clean(self):
        cleaned_data = super(PasswordResetForm2, self).clean()
        username = cleaned_data.get('username')
        code = cleaned_data.get('code')
        new_pass1 = cleaned_data.get('new_pass1')
        new_pass2 = cleaned_data.get('new_pass2')

        try:
            user = User.objects.get(username=username)
        except:
            self.add_error('username', 'No account with that Username found.')
            return

        try:
            print username
            userCode = UserReset.objects.get(username=username)
            print userCode
        except:
            self.add_error('username', 'Given username has not requested a code. If you require one, click the link at the top of the page.')
            return

        if userCode.code != int(code):
            self.add_error('code', 'Reset code is invalid.')
            return

        if new_pass1 != new_pass2:
            self.add_error('new_pass1', "Passwords didn't match")
            self.add_error('new_pass2', "Passwords didn't match")
