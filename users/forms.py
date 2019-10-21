from django import forms
from .models import User

class UserCreationThroughSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

#
#
# class DriverCreationForm(forms.ModelForm):
#     class Meta:
#         model = Driver
#         fields = ('first_name',)