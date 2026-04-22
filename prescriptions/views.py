from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Prescription, PrescriptionMedicine
from inventory.models import MedicineStock, InventoryLog
from .forms import PrescriptionForm, PrescriptionMedicineForm

@login_required
def prescription_list(request):
    if request.user.role == 'Doctor':
        prescriptions = Prescription.objects.filter(doctor=request.user).order_by('-created_at')
    else:
        prescriptions = Prescription.objects.all().order_by('-created_at')
        
    return render(request, 'prescriptions/prescription_list.html', {'prescriptions': prescriptions})

@login_required
def prescription_create(request):
    if request.user.role != 'Doctor':
        messages.error(request, "Only doctors can create prescriptions.")
        return redirect('prescription_list')
        
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = request.user
            prescription.save()
            messages.success(request, "Prescription draft created. Please add medicines.")
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        form = PrescriptionForm()
        
    return render(request, 'prescriptions/prescription_form.html', {'form': form})

@login_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    medicines = prescription.medicines.all()
    
    if request.method == 'POST' and request.user.role == 'Doctor' and prescription.status == 'Draft':
        form = PrescriptionMedicineForm(request.POST)
        if form.is_valid():
            pm = form.save(commit=False)
            pm.prescription = prescription
            pm.save()
            messages.success(request, "Medicine added to prescription.")
            return redirect('prescription_detail', pk=prescription.pk)
    else:
        form = PrescriptionMedicineForm()
        
    return render(request, 'prescriptions/prescription_detail.html', {
        'prescription': prescription,
        'medicines': medicines,
        'form': form
    })

@login_required
def prescription_finalize(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    if request.user.role == 'Doctor' and prescription.doctor == request.user and prescription.status == 'Draft':
        if not prescription.medicines.exists():
            messages.error(request, "Cannot finalize prescription without medicines.")
            return redirect('prescription_detail', pk=pk)
            
        prescription.status = 'Finalized'
        prescription.save()
        messages.success(request, "Prescription finalized.")
    return redirect('prescription_detail', pk=pk)

@login_required
def prescription_dispense(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    # Only Receptionist or Admin typically dispenses, but let's allow Receptionist
    if request.user.role in ['Receptionist', 'Admin'] and prescription.status == 'Finalized':
        try:
            with transaction.atomic():
                for pm in prescription.medicines.all():
                    stock = pm.medicine.stock
                    if stock.quantity < pm.quantity_prescribed:
                        raise ValueError(f"Not enough stock for {pm.medicine.name}")
                    
                    stock.quantity -= pm.quantity_prescribed
                    stock.save()
                    
                    InventoryLog.objects.create(
                        medicine=pm.medicine,
                        user=request.user,
                        action='DEDUCT',
                        quantity_changed=-pm.quantity_prescribed,
                        remarks=f"Dispensed for Prescription #{prescription.id}"
                    )
                
                prescription.status = 'Dispensed'
                prescription.save()
                messages.success(request, "Prescription dispensed and stock updated.")
        except ValueError as e:
            messages.error(request, str(e))
            
    return redirect('prescription_detail', pk=pk)
