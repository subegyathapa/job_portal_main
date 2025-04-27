# companies/forms.py
from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'description', 'website', 'location', 'established_date']
        widgets = {
            'established_date': forms.DateInput(attrs={'type': 'date'}),
        }