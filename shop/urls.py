from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('home', views.home, name='home'),
    path('store', views.store, name='store'),
]
