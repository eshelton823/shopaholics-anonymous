from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'shop/home.html')

def dashboard(request):
    return render(request, 'shop/dashboard.html')

def store(request):
    return render(request, 'shop/store.html')