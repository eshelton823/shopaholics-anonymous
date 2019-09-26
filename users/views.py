from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreationThroughSignupForm, DriverCreationForm



def user_signup(request):
    form = UserCreationThroughSignupForm(request.POST)
    return render(request, 'user_signup.html', {'form': form})


