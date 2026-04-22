from django.contrib import admin
from .models import Prescription, PrescriptionMedicine

class PrescriptionMedicineInline(admin.TabularInline):
    model = PrescriptionMedicine
    extra = 1

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('patient__name', 'doctor__username')
    inlines = [PrescriptionMedicineInline]

@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'medicine', 'quantity_prescribed', 'duration_days')
    search_fields = ('medicine__name', 'prescription__patient__name')
