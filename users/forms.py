from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.contrib.auth.models import User


#
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('url', 'location', 'company')


class UserCreationThroughSignupForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = '__all__'

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'
# #
# #
# class DriverCreationForm(forms.ModelForm):
#     class Meta:
#         model = Driver
#         fields = ('first_name',)