from django import forms
from .models import Prescription, PrescriptionMedicine

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes for this prescription...'}),
        }

class PrescriptionMedicineForm(forms.ModelForm):
    class Meta:
        model = PrescriptionMedicine
        fields = ['medicine', 'dosage_instructions', 'quantity_prescribed', 'duration_days']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'dosage_instructions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1 pill 3x a day'}),
            'quantity_prescribed': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control'}),
        }
