from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def home(request):
    return render(request, 'shop/home.html')

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'shop/dashboard.html')
    else:
        return redirect('/profile/signin')

def driver_dash(request):
    if request.user.is_authenticated:
        return render(request, 'shop/driver_dash.html')
    else:
        return redirect('/profile/signin')

def store(request):
    return render(request, 'shop/store.html')
