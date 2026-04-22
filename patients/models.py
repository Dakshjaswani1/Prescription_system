from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    
    # Medical Information
    medical_history = models.TextField(blank=True, null=True, help_text="Past illnesses, surgeries, chronic conditions")
    allergies = models.TextField(blank=True, null=True, help_text="Known drug allergies and sensitivities")
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.contact_number})"
