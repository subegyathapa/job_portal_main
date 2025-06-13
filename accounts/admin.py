from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


admin.site.unregister(User)


class CustomUserAdmin(UserAdmin):
    actions = None
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_employer', 'phone_number']
    list_filter = ['is_employer']
    search_fields = ['user__username', 'user__email', 'phone_number']
    actions = None
