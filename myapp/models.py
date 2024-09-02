from django.db import models
from django.contrib.auth.models import User
import re

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    domain=models.CharField(max_length=100)
    year_founded = models.FloatField()
    industry = models.CharField(max_length=200)
    size_range = models.CharField(max_length=50, blank=True, null=True)
    
    locality=models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    linkedin_url = models.URLField(max_length=500, null=True, blank=True)
    current_employee_estimate = models.IntegerField(null=True, blank=True)
    total_employee_estimate = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    
    def __str__(self):
        return f"{self.name}"
    
class files(models.Model):
    file = models.FileField(upload_to='uploads', blank=True, null=True)   
    