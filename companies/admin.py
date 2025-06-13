# companies/admin.py
from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'location', 'website']
    list_filter = ['location']
    search_fields = ['name', 'owner__username', 'location']
    actions = None