from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def home(request):
    return render(request, 'shop/home.html')

def dashboard(request):
    print(request.user)
    if request.user.username != "":
        return render(request, 'shop/dashboard.html')
    else:
        return redirect('/profile/signin')

def driver_dash(request):
    if request.user.driver_filled:
        return render(request, 'shop/driver_dash.html')
    else:
        return redirect('/users/driver_info.html')

def store(request):
    return render(request, 'shop/store.html')
