from django.urls import path
from django.conf.urls import include
from users.views import UserViewSet
from users import views
from rest_framework import routers



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = "users"

urlpatterns = [
    path('signup/', views.user_signup, name='user_signup'),
    path('signin/', views.user_signin, name='user_signin'),
]
