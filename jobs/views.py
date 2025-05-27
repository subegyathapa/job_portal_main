# jobs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application, Category
from .forms import JobForm, ApplicationForm, JobSearchForm


def job_list(request):
    form = JobSearchForm(request.GET)
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')

    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        location = form.cleaned_data.get('location')
        category = form.cleaned_data.get('category')
        job_type = form.cleaned_data.get('job_type')

        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(requirements__icontains=keyword)
            )

        if location:
            jobs = jobs.filter(location__icontains=location)

        if category:
            jobs = jobs.filter(category=category)

        if job_type:
            jobs = jobs.filter(job_type=job_type)

    categories = Category.objects.all()
    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'form': form,
        'categories': categories,
        'show_hero': True


    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    already_applied = False

    if request.user.is_authenticated:
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'already_applied': already_applied
    })


@login_required
def job_create(request):
    if not request.user.profile.is_employer:
        messages.error(request, 'Only employers can post jobs.')
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.user, request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(request.user)

    return render(request, 'jobs/job_form.html', {'form': form})


@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)

    if request.method == 'POST':
        form = JobForm(request.user, request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm(request.user, instance=job)

    return render(request, 'jobs/job_form.html', {'form': form, 'job': job})


@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('job_list')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@login_required
def apply_for_job(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)

    if request.user.profile.is_employer:
        messages.error(request, 'Employers cannot apply for jobs.')
        return redirect('job_detail', pk=job.pk)

    already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    if already_applied:
        messages.error(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=job.pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user

            # Use the user's resume if they don't upload a new one
            if not application.resume and request.user.profile.resume:
                application.resume = request.user.profile.resume

            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', pk=job.pk)  # Redirect back to job detail
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply_form.html', {'form': form, 'job': job})

@login_required
def manage_applications(request, job_pk):
    job = get_object_or_404(Job, pk=job_pk, posted_by=request.user)
    applications = job.applications.all()

    return render(request, 'jobs/manage_applications.html', {
        'job': job,
        'applications': applications
    })


@login_required
def update_application_status(request, application_pk, status):
    application = get_object_or_404(Application, pk=application_pk, job__posted_by=request.user)

    if status in dict(Application.STATUS_CHOICES).keys():
        application.status = status
        application.save()
        messages.success(request, f'Application status updated to {dict(Application.STATUS_CHOICES)[status]}.')
    else:
        messages.error(request, 'Invalid status.')

    return redirect('manage_applications', job_pk=application.job.pk)


# jobs/views.py
@login_required
def cancel_application(request, pk):
    # Get the application by ID, ensuring it belongs to the current user
    application = get_object_or_404(Application, pk=pk, applicant=request.user)

    if request.method == 'POST':
        job_title = application.job.title
        application.delete()
        messages.success(request, f'Your application for "{job_title}" has been cancelled.')
        return redirect('dashboard')

    return render(request, 'jobs/cancel_application.html', {'application': application})


@login_required
def withdraw_application(request, job_pk):
    # Alternative approach: cancel by job ID
    job = get_object_or_404(Job, pk=job_pk)
    application = get_object_or_404(Application, job=job, applicant=request.user)

    if request.method == 'POST':
        application.delete()
        messages.success(request, f'Your application for "{job.title}" has been withdrawn.')
        return redirect('job_detail', pk=job.pk)

    return render(request, 'jobs/cancel_application.html', {'application': application})