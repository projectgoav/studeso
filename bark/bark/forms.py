from django import forms
from django.contrib.auth.models import User
from rango.models import UserProfile

#Get data for user when they sign up
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

#Get data for the User Profile
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture')