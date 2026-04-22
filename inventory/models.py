from django.db import models
from accounts.models import User

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    strength = models.CharField(max_length=100, help_text="e.g., 500mg, 10ml")
    minimum_stock_threshold = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} {self.strength}"

class MedicineStock(models.Model):
    medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField(default=0)
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.medicine.name} - {self.quantity} in stock"

class InventoryLog(models.Model):
    ACTION_CHOICES = (
        ('ADD', 'Stock Added'),
        ('DEDUCT', 'Stock Deducted'),
        ('ADJUST', 'Manual Adjustment'),
    )

    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='inventory_logs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    quantity_changed = models.IntegerField(help_text="Positive for addition, negative for deduction")
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.medicine.name} - {self.action} ({self.quantity_changed}) by {self.user}"
