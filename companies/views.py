# companies/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company
from .forms import CompanyForm


@login_required
def company_list(request):
    companies = Company.objects.filter(owner=request.user)
    return render(request, 'companies/company_list.html', {'companies': companies})


@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    jobs = company.jobs.all()
    return render(request, 'companies/company_detail.html', {'company': company, 'jobs': jobs})


@login_required
def company_create(request):
    if not request.user.profile.is_employer:
        messages.error(request, 'Only employers can create companies.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = request.user
            company.save()
            messages.success(request, 'Company created successfully!')
            return redirect('company_detail', pk=company.pk)
    else:
        form = CompanyForm()

    return render(request, 'companies/company_form.html', {'form': form})


@login_required
def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('company_detail', pk=company.pk)
    else:
        form = CompanyForm(instance=company)

    return render(request, 'companies/company_form.html', {'form': form, 'company': company})


@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == 'POST':
        company.delete()
        messages.success(request, 'Company deleted successfully!')
        return redirect('company_list')

    return render(request, 'companies/company_confirm_delete.html', {'company': company})