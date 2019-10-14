from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('home', views.home, name='home'),
    path('store', views.store, name='store'),
]
