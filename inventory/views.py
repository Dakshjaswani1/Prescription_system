from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medicine, MedicineStock, InventoryLog
from .forms import MedicineForm, MedicineStockForm
from django.db import transaction

@login_required
def medicine_list(request):
    medicines = Medicine.objects.all().select_related('stock').order_by('name')
    return render(request, 'inventory/medicine_list.html', {'medicines': medicines})

@login_required
def medicine_create(request):
    if request.method == 'POST':
        med_form = MedicineForm(request.POST)
        stock_form = MedicineStockForm(request.POST)
        if med_form.is_valid() and stock_form.is_valid():
            with transaction.atomic():
                medicine = med_form.save()
                stock = stock_form.save(commit=False)
                stock.medicine = medicine
                stock.save()
                
                # Log the addition
                InventoryLog.objects.create(
                    medicine=medicine,
                    user=request.user,
                    action='ADD',
                    quantity_changed=stock.quantity,
                    remarks="Initial stock added"
                )
            messages.success(request, 'Medicine and initial stock added successfully.')
            return redirect('medicine_list')
    else:
        med_form = MedicineForm()
        stock_form = MedicineStockForm()
        
    return render(request, 'inventory/medicine_form.html', {
        'med_form': med_form,
        'stock_form': stock_form,
        'title': 'Add New Medicine'
    })

@login_required
def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine.objects.select_related('stock'), pk=pk)
    logs = medicine.inventory_logs.all().order_by('-timestamp')[:50]
    return render(request, 'inventory/medicine_detail.html', {'medicine': medicine, 'logs': logs})
