from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UserCreationThroughSignupForm
from users.models import User
from rest_framework import viewsets
from users.serializers import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

def user_signup(request):
    form = UserCreationThroughSignupForm(request.POST)
    return render(request, 'users/user_signup.html', {'form': form})
def user_signin(request):
    return render(request, 'users/user_signin.html')

def driver_info(request):
    return render(request, 'users/driver_info.html')
