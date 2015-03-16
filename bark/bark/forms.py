from django import forms
from django.contrib.auth.models import User
from bark.models import UserProfile, Post
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
