# companies/models.py
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100)
    established_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"