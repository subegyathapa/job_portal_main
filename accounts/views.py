# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from jobs.models import Application


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set the is_employer field in the user's profile
            user.profile.is_employer = form.cleaned_data.get('is_employer')
            user.profile.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def dashboard(request):
    user = request.user

    if user.profile.is_employer:
        # For employers, show their companies and posted jobs
        context = {
            'companies': user.companies.all(),
            'posted_jobs': user.posted_jobs.all(),
        }
        return render(request, 'accounts/employer_dashboard.html', context)
    else:
        # For job seekers, show their applications
        applications = Application.objects.filter(applicant=user)
        return render(request, 'accounts/jobseeker_dashboard.html', {'applications': applications})



# accounts/views.py
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('login')  # or wherever you want to redirect after logout