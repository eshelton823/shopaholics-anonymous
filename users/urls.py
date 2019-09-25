from django.urls import path
from .import views

urlpatterns = [
    path('signup/', views.user_signup, name='user_signup'),
]