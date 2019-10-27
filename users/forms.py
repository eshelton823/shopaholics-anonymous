from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class UserCreationThroughSignupForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = '__all__'
#
#
# class DriverCreationForm(forms.ModelForm):
#     class Meta:
#         model = Driver
#         fields = ('first_name',)