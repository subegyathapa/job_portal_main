# accounts/admin.py
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_employer', 'phone_number']
    list_filter = ['is_employer']
    search_fields = ['user__username', 'user__email', 'phone_number']