from django.urls import path

from . import views


app_name = "payments"

urlpatterns = [
    path('charge/', views.charge, name='charge'),
    path('stripe-payment/', views.HomePageView.as_view(), name='home'),
]