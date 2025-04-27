# jobs/forms.py
from django import forms
from .models import Job, Application, Category


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company', 'category', 'description', 'requirements',
                  'salary_min', 'salary_max', 'location', 'job_type', 'deadline', 'is_active']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        # Only show companies owned by the current user
        self.fields['company'].queryset = user.companies.all()


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'placeholder': 'Write your cover letter here...'}),
        }


class JobSearchForm(forms.Form):
    keyword = forms.CharField(required=False, label='Keyword')
    location = forms.CharField(required=False, label='Location')
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    job_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Job.JOB_TYPE_CHOICES,
        required=False,
        label='Job Type'
    )