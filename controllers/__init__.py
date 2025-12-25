from typing import Optional
from datetime import datetime, time
from models import User, UserRole, Patient, Doctor, TimeSlot, Appointment
from services import AuthService, AppointmentService

class AppController:
    def __init__(self):
        self.auth = AuthService()
        self.appt_service = AppointmentService()
        self._seed_data()
    
    def _seed_data(self):
        doc = self.auth.register_doctor(
            "Dr. Arjun Rao",
            "arjun@medibook.local",
            "doctor123",
            speciality="Cardiologist",
            exp_yrs=8,
            location="Hyderabad",
            mode="In-person"
        )
        self.appt_service.add_doctor(doc)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for h in [10, 11, 12, 15, 16]:
            slot = TimeSlot.create(
                doctor_id=doc.id,
                date=today,
                start_time=time(hour=h),
                end_time=time(hour=h + 1),
            )
            self.appt_service.add_slot(slot)
    
    def login(self, email: str, password: str) -> Optional[User]:
        return self.auth.login(email, password)
    
    def register_patient(self, name, email, password, **extra) -> Patient:
        return self.auth.register_patient(name, email, password, **extra)
    
    def get_doctors(self, speciality: str | None = None):
        return self.appt_service.list_doctors(speciality)
    
    def get_doctor_slots(self, doctor_id: str, date: datetime | None = None):
        return self.appt_service.get_doctor_slots(doctor_id, date)
    
    def book_appointment(self, patient: Patient, doctor: Doctor, slot_id: str):
        return self.appt_service.book(patient, doctor, slot_id)
    
    def cancel_appointment(self, patient: Patient, appointment_id: str):
        self.appt_service.cancel(appointment_id, patient)
    
    def get_patient_appointments(self, patient: Patient):
        return self.appt_service.list_patient_appointments(patient)
