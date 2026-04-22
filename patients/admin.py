from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'contact_number', 'status', 'created_at')
    list_filter = ('status', 'gender')
    search_fields = ('name', 'contact_number')
