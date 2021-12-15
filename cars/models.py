from django.core.validators import RegexValidator
from django.db import models


class Driver(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vehicle(models.Model):
    driver_id = models.ForeignKey('Driver', on_delete=models.CASCADE, null=True)
    make = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    plate_number = models.CharField(validators=(RegexValidator(regex="^\w\w \d{4} \w\w$"),), unique=True, max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
