from django.contrib import admin
from .models import Medicine, MedicineStock, InventoryLog

class MedicineStockInline(admin.StackedInline):
    model = MedicineStock
    extra = 0

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manufacturer', 'strength', 'minimum_stock_threshold')
    search_fields = ('name', 'manufacturer')
    inlines = [MedicineStockInline]

@admin.register(MedicineStock)
class MedicineStockAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'quantity', 'batch_number', 'expiry_date')
    search_fields = ('medicine__name', 'batch_number')

@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'action', 'quantity_changed', 'user', 'timestamp')
    list_filter = ('action',)
    search_fields = ('medicine__name', 'user__username')
