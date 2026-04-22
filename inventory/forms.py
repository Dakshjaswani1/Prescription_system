from django import forms
from .models import Medicine, MedicineStock

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'manufacturer', 'strength', 'minimum_stock_threshold']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'strength': forms.TextInput(attrs={'class': 'form-control'}),
            'minimum_stock_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MedicineStockForm(forms.ModelForm):
    class Meta:
        model = MedicineStock
        fields = ['quantity', 'batch_number', 'expiry_date']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'batch_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
