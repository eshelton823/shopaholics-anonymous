from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from .forms import UserCreationThroughSignupForm
from users.models import Profile
from rest_framework import viewsets
from users.serializers import UserSerializer



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

def user_signup(request):
    if request.user.is_authenticated:
        return render(request, 'shop/dashboard.html')
    form = UserCreationThroughSignupForm(request.POST)
    return render(request, 'users/user_signup.html', {'form': form})

def user_signin(request):
    return render(request, 'users/user_signin.html')

def driver_info(request):
    return render(request, 'users/driver_info.html')


def add_driver_info(request):
    if request.method == "POST":
        try:
            u = request.user.profile
            u.license_plate_number = request.POST['licensePlateNumberInput']
            u.car_make = request.POST['carMakeInput']
            u.car_model = request.POST['carModelInput']
            u.license_identifier_number = request.POST['driverLicenseNumberInput']
            u.state_of_drivers_license_issuance = request.POST['stateOfLicenseIssuanceInput']
            u.driver_filled = True
            u.save()
            return HttpResponseRedirect(reverse('shop:driver_dash'))
        except:
            print("smaller fail")
            return HttpResponseRedirect(reverse('shop:failure'))
    print("big fail")
    return HttpResponseRedirect(reverse('shop:failure'))
