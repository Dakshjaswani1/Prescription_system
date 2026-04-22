from django.db import models
from accounts.models import User
from patients.models import Patient
from inventory.models import Medicine

class Prescription(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Finalized', 'Finalized'),
        ('Dispensed', 'Dispensed'),
    )

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions_created')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Draft')
    notes = models.TextField(blank=True, null=True, help_text="Additional notes from the doctor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription #{self.id} for {self.patient.name}"

class PrescriptionMedicine(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage_instructions = models.CharField(max_length=255, help_text="e.g., 1 pill 3 times a day")
    quantity_prescribed = models.PositiveIntegerField()
    duration_days = models.PositiveIntegerField(help_text="Number of days to take the medicine")

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity_prescribed} for {self.prescription}"
