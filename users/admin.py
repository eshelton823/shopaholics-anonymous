from django.contrib import admin
from .models import Profile, Order
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
# from .forms import UserForm, ProfileForm
# class ProfileAdmin(UserAdmin):
#     add_form = ProfileForm
#     # form = CustomUserChangeForm
#     model = Profile
#     list_display = '__all__'
admin.site.register(Profile)
admin.site.register(Order)
# admin.site.register(Driver)
