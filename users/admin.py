from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserCreationThroughSignupForm, CustomUserChangeForm

class ProfileAdmin(UserAdmin):
    add_form = UserCreationThroughSignupForm
    form = CustomUserChangeForm
    model = Profile
    list_display = '__all__'
admin.site.register(Profile)
# admin.site.register(Driver)