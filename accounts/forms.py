# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_employer = forms.BooleanField(required=False, label='Register as an Employer')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_employer']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'resume', 'profile_picture', 'skills']
        widgets = {
            'skills': forms.Textarea(attrs={'placeholder': 'Enter your skills separated by commas'}),
        }