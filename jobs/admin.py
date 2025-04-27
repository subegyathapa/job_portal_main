# jobs/admin.py
from django.contrib import admin
from .models import Category, Job, Application

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'job_type', 'created_at', 'deadline', 'is_active']
    list_filter = ['job_type', 'is_active', 'created_at', 'deadline']
    search_fields = ['title', 'company__name', 'location']
    date_hierarchy = 'created_at'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['job__title', 'applicant__username']
    date_hierarchy = 'applied_at'