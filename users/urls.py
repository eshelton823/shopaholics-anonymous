from django.urls import path
from users import views



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = "users"

urlpatterns = [
    path('signup/', views.user_signup, name='user_signup'),
    path('signin/', views.user_signin, name='user_signin'),
    path('driver_info/', views.driver_info, name='driver_info'),
    path('add_driver_info/', views.add_driver_info, name='add_driver_info'),
    path('driver_edit_form/', views.driver_edit_form, name='driver_edit_form'),
    path('create_account/', views.create_account, name='create_account'),
    path('validate_login/', views.validate_login, name='validate_login'),

]
