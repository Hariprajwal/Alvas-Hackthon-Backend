import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from APIs.models import User, Patient, ScanLog
import random

def populate():
    # Ensure testuser exists
    doctor, created = User.objects.get_or_create(
        username="testuser",
        defaults={
            "email": "doctor@example.com",
            "role": "doctor",
            "is_verified": True
        }
    )
    if created:
        doctor.set_password("TestPassword123")
        doctor.save()
        print("Created testuser doctor.")
    else:
        # Just in case it's not verified
        doctor.is_verified = True
        doctor.save()
        print("Found testuser doctor.")

    # Create dummy patients
    patients_data = [
        {"name": "Sarah Connor", "age": 45, "gender": "Female", "phone": "555-0101", "email": "sarah.connor@example.com", "risk_zone": "high"},
        {"name": "John Smith", "age": 32, "gender": "Male", "phone": "555-0102", "email": "john.smith@example.com", "risk_zone": "low"},
        {"name": "Emily Chen", "age": 58, "gender": "Female", "phone": "555-0103", "email": "emily.chen@example.com", "risk_zone": "medium"},
    ]

    for data in patients_data:
        patient, p_created = Patient.objects.get_or_create(
            user=doctor,
            name=data["name"],
            defaults={
                "age": data["age"],
                "gender": data["gender"],
                "phone": data["phone"],
                "email": data["email"],
                "risk_zone": data["risk_zone"]
            }
        )
        if p_created:
            print(f"Created patient {patient.name}")
        
        # Create a dummy scan log for them if they don't have one
        if not ScanLog.objects.filter(patient=patient).exists():
            risk_score = 10.0 if data["risk_zone"] == "low" else (50.0 if data["risk_zone"] == "medium" else 85.0)
            predicted = "Melanocytic Nevus" if risk_score < 40 else ("Basal Cell Carcinoma" if risk_score < 70 else "Melanoma")
            category = "LOW" if risk_score < 44 else ("MEDIUM" if risk_score < 67 else "HIGH")
            
            ScanLog.objects.create(
                patient=patient,
                image="scans/dummy.jpg", # We don't have a real image, but this is fine for DB
                predicted_disease=predicted,
                confidence=95.0,
                risk_score=risk_score,
                risk_category=category,
                all_probs={"nv": 95.0, "mel": 5.0} if category == "LOW" else {"mel": 85.0, "nv": 15.0},
                notes=f"Initial assessment for {patient.name}. Risk zone categorized as {data['risk_zone']}."
            )
            print(f"Created dummy scan log for {patient.name}")

if __name__ == '__main__':
    populate()
    print("Database populated successfully!")
