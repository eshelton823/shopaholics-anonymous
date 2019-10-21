from django.urls import path, include

from . import views



app_name = "shop"

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('driver_dash', views.driver_dash, name='driver_dash'),
    path('home', views.home, name='home'),
    path('store', views.store, name='store'),

]
