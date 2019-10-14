from django.urls import path
from .import views

app_name = "users"

urlpatterns = [
    path('signup/', views.user_signup, name='user_signup'),
    path('signin/', views.user_signin, name='user_signin'),
]
