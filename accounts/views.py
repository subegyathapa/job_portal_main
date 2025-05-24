# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from jobs.models import Application
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy,reverse


# accounts/views.py
def register(request):
    next_url = request.GET.get('next')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.is_employer = form.cleaned_data.get('is_employer')
            user.profile.save()
            messages.success(request, 'Your account has been created! You can now log in.')

            # Redirect to login with next parameter if it exists
            if next_url:
                return redirect(f"{reverse('login')}?next={next_url}")
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'next_url': next_url
    })

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
        context = {
            'applications': applications
        }
        return render(request, 'accounts/jobseeker_dashboard.html', context)


# accounts/views.py
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('login')  # or wherever you want to redirect after logout


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        # First check if there's a 'next' parameter
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url

        # If no 'next' parameter, redirect based on user type
        if self.request.user.profile.is_employer:
            return reverse_lazy('dashboard')  # Employers go to dashboard
        else:
            return reverse_lazy('job_list')  # Job seekers go to job list