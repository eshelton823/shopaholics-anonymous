from django import forms
from .models import Profile

class UserCreationThroughSignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

#
#
# class DriverCreationForm(forms.ModelForm):
#     class Meta:
#         model = Driver
#         fields = ('first_name',)