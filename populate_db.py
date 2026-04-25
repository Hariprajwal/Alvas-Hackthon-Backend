import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from APIs.models import User, Patient, ScanLog, Prescription
from django.utils import timezone

def populate():
    # 1. Create Demo Users
    users = [
        {'username': 'doctor',  'role': 'doctor',  'first_name': 'Sarah', 'last_name': 'Smith'},
        {'username': 'nurse',   'role': 'nurse',   'first_name': 'Joy',   'last_name': 'Hacker'},
        {'username': 'patient', 'role': 'patient', 'first_name': 'Julian', 'last_name': 'Weaver'},
    ]
    
    for u in users:
        user, created = User.objects.get_or_create(username=u['username'])
        user.role = u['role']
        user.first_name = u['first_name']
        user.last_name = u['last_name']
        user.is_verified = True
        user.set_password('password123')
        user.save()
        print(f"User {u['username']} ready ({user.first_name}).")

    # 2. Create some sample patients
    # We need to link patients to a user (e.g. the doctor)
    doctor = User.objects.get(username='doctor')
    
    patients_data = [
        {'name': 'Julian Weaver', 'age': 54, 'gender': 'Male', 'email': 'julian@example.com', 'phone': '9876543210'},
        {'name': 'Emma Thompson', 'age': 29, 'gender': 'Female', 'email': 'emma@example.com', 'phone': '9876543211'},
    ]
    
    for p in patients_data:
        patient, created = Patient.objects.get_or_create(
            name=p['name'],
            user=doctor,
            defaults={'age': p['age'], 'gender': p['gender'], 'email': p['email'], 'phone': p['phone']}
        )
        print(f"Patient {p['name']} ready.")

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
