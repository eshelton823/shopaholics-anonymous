from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from .forms import UserCreationThroughSignupForm
from users.models import Profile, User
from rest_framework import viewsets
from users.serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

def user_signup(request, context={'email':"", 'username':""}):
    if request.user.is_authenticated:
        return render(request, 'shop/dashboard.html')
    form = UserCreationThroughSignupForm(request.POST)
    return render(request, 'users/user_signup.html', context)

def user_signin(request):
    return render(request, 'users/user_signin.html')

def driver_info(request):
    return render(request, 'users/driver_info.html')

def validate_login(request):
    if request.method == "POST":
        try:
            if len(User.objects.filter(username=request.POST['username'])) == 0:
                context = {}
                context['password'] = ""
                context['username'] = "Incorrect Username"
                return render(request, 'users/user_signin.html', context)
            u = User.objects.get(username=request.POST['username'])
            check = check_password(request.POST['password'], u.password)
            if not check:
                context = {}
                context['username'] = ""
                context['password'] = "Incorrect Password"
                return render(request, 'users/user_signin.html', context)
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('shop:dashboard'))
        except:
            print("smaller fail")
            return HttpResponseRedirect(reverse('shop:failure'))
    print("big fail")
    return HttpResponseRedirect(reverse('shop:dashboard'))


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

def driver_edit_form(request):
    context = get_info(request.user)
    return render(request, 'users/edit_driver_info.html', context)


def create_account(request):
    if request.method == "POST":
        try:
            print(User.objects.filter(username="ejs"))
            if len(User.objects.filter(username=request.POST['username'])) != 0:
                print("Username duplicate")
                context = {}
                context['email'] = ""
                context['username'] = "That username is already taken"
                print("here")
                return render(request, 'users/user_signup.html', context)
            elif len(User.objects.filter(email=request.POST['email'])) != 0:
                print("Email duplicate")
                context = {}
                context['username'] = ""
                context['email'] = "That email is already taken"
                print("here2")
                return render(request, 'users/user_signup.html', context)
            # print("here3")
            u = User(username=request.POST['username'], password=make_password(request.POST['password']), email=request.POST['email'], first_name=request.POST['firstname'], last_name=request.POST['lastname'])
            u.save()
            u1 = User.objects.get(email=request.POST['email'])
            u1.profile.email = request.POST['email']
            u1.save()
            return HttpResponseRedirect(reverse('shop:dashboard'))
        except:
            print("smaller fail")
            return HttpResponseRedirect(reverse('shop:failure'))
    print("big fail")
    return HttpResponseRedirect(reverse('shop:failure'))


# def edit_driver_info(request):
#     if request.method == "POST":
#         try:
#             u = request.user.profile
#
#             u.save()
#             return HttpResponseRedirect(reverse('shop:dashboard'))
#         except:
#             print("smaller fail")
#             return HttpResponseRedirect(reverse('shop:failure'))
#     print("big fail")
#     return HttpResponseRedirect(reverse('shop:failure'))


def get_info(d):
    context = {}
    context['plate'] = d.profile.license_plate_number
    context['make'] = d.profile.car_make
    context['model'] = d.profile.car_model
    context['license'] = d.profile.license_identifier_number
    context['state'] = d.profile.state_of_drivers_license_issuance
    return context