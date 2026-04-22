import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User
from patients.models import Patient
from inventory.models import Medicine, MedicineStock, InventoryLog
from prescriptions.models import Prescription, PrescriptionMedicine

def seed_data():
    print("Seeding Users...")
    doctor, _ = User.objects.get_or_create(username='doctor1', defaults={'email': 'doc@example.com', 'first_name': 'Sarah', 'last_name': 'Connor', 'role': 'Doctor'})
    if _: doctor.set_password('pass123')
    doctor.save()
    
    receptionist, _ = User.objects.get_or_create(username='receptionist1', defaults={'email': 'rec@example.com', 'first_name': 'John', 'last_name': 'Smith', 'role': 'Receptionist'})
    if _: receptionist.set_password('pass123')
    receptionist.save()

    print("Seeding Patients...")
    patient_names = ["Alice Williams", "Bob Johnson", "Charlie Brown", "Diana Prince", "Ethan Hunt", 
                     "Fiona Gallagher", "George Costanza", "Hannah Abbott", "Ian Malcolm", "Julia Roberts"]
    patients = []
    for i, name in enumerate(patient_names):
        p, created = Patient.objects.get_or_create(
            name=name,
            defaults={
                'age': random.randint(18, 80),
                'gender': random.choice(['M', 'F']),
                'contact_number': f"555-010{i}",
                'address': f"{i*10} Main St, Cityville",
                'medical_history': "None" if random.random() > 0.3 else "Hypertension, asthma",
                'allergies': "None" if random.random() > 0.2 else random.choice(["Penicillin", "Peanuts", "Aspirin", "Sulfa drugs"]),
                'status': 'Active'
            }
        )
        patients.append(p)

    print("Seeding Medicines...")
    medicine_data = [
        ("Paracetamol", "500mg", "PharmaCorp"), ("Ibuprofen", "400mg", "PharmaCorp"),
        ("Amoxicillin", "250mg", "HealthMed"), ("Azithromycin", "500mg", "HealthMed"),
        ("Metformin", "500mg", "BioLab"), ("Atorvastatin", "20mg", "BioLab"),
        ("Amlodipine", "5mg", "HeartCare"), ("Omeprazole", "20mg", "GutMed"),
        ("Lisinopril", "10mg", "HeartCare"), ("Levothyroxine", "50mcg", "BioLab"),
        ("Ciprofloxacin", "500mg", "HealthMed"), ("Losartan", "50mg", "HeartCare"),
        ("Cetirizine", "10mg", "AllergyRelief"), ("Gabapentin", "300mg", "NeuroPharma"),
        ("Sertraline", "50mg", "MindCare"), ("Fluoxetine", "20mg", "MindCare"),
        ("Furosemide", "40mg", "HeartCare"), ("Pantoprazole", "40mg", "GutMed"),
        ("Albuterol", "90mcg", "BreathWell"), ("Tramadol", "50mg", "PainMed"),
        ("Meloxicam", "15mg", "PainMed"), ("Cyclobenzaprine", "10mg", "NeuroPharma"),
        ("Clopidogrel", "75mg", "HeartCare"), ("Trazodone", "50mg", "MindCare"),
        ("Duloxetine", "30mg", "MindCare")
    ]
    
    medicines = []
    for name, strength, manu in medicine_data:
        med, created = Medicine.objects.get_or_create(
            name=name, strength=strength, manufacturer=manu,
            defaults={'minimum_stock_threshold': random.randint(20, 50)}
        )
        medicines.append(med)
        if created:
            stock = MedicineStock.objects.create(
                medicine=med, quantity=random.randint(50, 500),
                batch_number=f"BATCH-{random.randint(1000, 9999)}",
                expiry_date=timezone.now().date() + timedelta(days=random.randint(100, 1000))
            )
            InventoryLog.objects.create(
                medicine=med, user=receptionist, action='ADD',
                quantity_changed=stock.quantity, remarks="Initial dummy stock"
            )

    print("Seeding Prescriptions...")
    if not Prescription.objects.exists():
        for i in range(5):
            prescription = Prescription.objects.create(
                doctor=doctor, patient=random.choice(patients),
                status=random.choice(['Finalized', 'Dispensed', 'Draft']),
                notes="Take after meals."
            )
            for _ in range(random.randint(1, 3)):
                pm, created = PrescriptionMedicine.objects.get_or_create(
                    prescription=prescription,
                    medicine=random.choice(medicines),
                    defaults={
                        'dosage_instructions': "1 pill twice a day",
                        'quantity_prescribed': random.randint(10, 30),
                        'duration_days': random.randint(5, 15)
                    }
                )
    
    print("Dummy data generation complete!")

if __name__ == '__main__':
    seed_data()
