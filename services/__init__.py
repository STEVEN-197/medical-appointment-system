from typing import Dict, List, Optional
from datetime import datetime, time
from models import User, Patient, Doctor, TimeSlot, Appointment, UserRole, AppointmentStatus
import google.generativeai as genai
import os
import json

class AuthService:
    def __init__(self):
        self._users_by_email: Dict[str, User] = {}
    def register_patient(self, name, email, password, **extra) -> Patient:
        if email.lower() in self._users_by_email:
            raise ValueError("Email already in use")
        patient = Patient.create(name, email, password, **extra)
        self._users_by_email[patient.email] = patient
        return patient
    def register_doctor(self, name, email, password, speciality, **extra) -> Doctor:
        if email.lower() in self._users_by_email:
            raise ValueError("Email already in use")
        doctor = Doctor.create(name, email, password, speciality, **extra)
        self._users_by_email[doctor.email] = doctor
        return doctor
    def login(self, email: str, password: str) -> Optional[User]:
        user = self._users_by_email.get(email.lower())
        if not user or not user.check_password(password):
            return None
        return user

class AppointmentService:
    def __init__(self):
        self.doctors: Dict[str, Doctor] = {}
        self.slots: Dict[str, TimeSlot] = {}
        self.appointments: Dict[str, Appointment] = {}
    def add_doctor(self, doctor: Doctor):
        self.doctors[doctor.id] = doctor
    def list_doctors(self, speciality: str | None = None) -> List[Doctor]:
        docs = list(self.doctors.values())
        if speciality:
            docs = [d for d in docs if d.speciality.lower() == speciality.lower()]
        return docs
    def add_slot(self, slot: TimeSlot):
        self.slots[slot.slot_id] = slot
    def get_doctor_slots(self, doctor_id: str, date: datetime | None = None) -> List[TimeSlot]:
        res = [s for s in self.slots.values() if s.doctor_id == doctor_id]
        if date:
            res = [s for s in res if s.date.date() == date.date()]
        return sorted(res, key=lambda s: (s.date, s.start_time))
    def book(self, patient: Patient, doctor: Doctor, slot_id: str) -> Appointment:
        slot = self.slots.get(slot_id)
        if not slot or slot.doctor_id != doctor.id:
            raise ValueError("Invalid slot")
        if slot.is_booked:
            raise ValueError("Slot already booked")
        appt = Appointment.create(patient.id, doctor.id, slot.slot_id)
        slot.mark_booked()
        self.appointments[appt.appointment_id] = appt
        return appt
    def cancel(self, appointment_id: str, patient: Patient):
        appt = self.appointments.get(appointment_id)
        if not appt or appt.patient_id != patient.id:
            raise ValueError("Appointment not found")
        appt.cancel()
        slot = self.slots.get(appt.slot_id)
        if slot:
            slot.mark_free()
    def list_patient_appointments(self, patient: Patient) -> List[Appointment]:
        return [a for a in self.appointments.values() if a.patient_id == patient.id]

class AIRecommendationService:
    def __init__(self, appointment_service: AppointmentService):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.appointment_service = appointment_service
    def _build_context(self, speciality: str | None = None) -> str:
        doctors = self.appointment_service.list_doctors(speciality)
        lines = []
        for d in doctors:
            slots = self.appointment_service.get_doctor_slots(d.id)
            free_slots = [s for s in slots if not s.is_booked]
            for s in free_slots:
                lines.append(f"Doctor {d.name} ({d.speciality}), doctor_id={d.id}, slot_id={s.slot_id}, date={s.date.date()}, start={s.start_time}, end={s.end_time}")
        return "\n".join(lines) or "No free slots."
    def recommend_slot(self, patient: Patient, speciality: Optional[str], urgency: str, constraints: Dict | None = None) -> Optional[Dict]:
        constraints = constraints or {}
        context = self._build_context(speciality)
        prompt = f"Patient: {patient.name}\nUrgency: {urgency}\nConstraints: {constraints}\nAvailable slots:\n{context}\nReturn JSON with doctor_id, slot_id, reason."
        try:
            resp = self.model.generate_content(prompt)
            text = resp.text.strip()
            start, end = text.find("{"), text.rfind("}") + 1
            return json.loads(text[start:end])
        except:
            return None
    def parse_natural_query(self, text: str) -> Dict:
        prompt = f"Parse: \"{text}\"\nReturn JSON with speciality, urgency, preferred_time_of_day, date_hint (or null if missing)."
        try:
            resp = self.model.generate_content(prompt)
            text_out = resp.text.strip()
            start, end = text_out.find("{"), text_out.rfind("}") + 1
            return json.loads(text_out[start:end])
        except:
            return {}
