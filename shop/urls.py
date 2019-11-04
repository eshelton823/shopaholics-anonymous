from django.urls import path, include

from . import views



app_name = "shop"

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('driver_dash', views.driver_dash, name='driver_dash'),
    path('home', views.home, name='home'),
    path('store', views.store, name='store'),
    path('process_order', views.process_order, name='process_order'),
    path('success', views.success, name='success'),
    path('failure', views.failure, name='failure'),
    path('reset', views.reset, name="reset"),
    path('match', views.match, name="match"),
    path('search', views.search, name="search"),

]
