from dataclasses import dataclass
from enum import Enum
import uuid
import hashlib
from datetime import datetime, time

class UserRole(str, Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"

class AppointmentStatus(str, Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: str
    role: UserRole
    @classmethod
    def create(cls, name, email, password, role):
        return cls(str(uuid.uuid4()), name, email.lower(), _hash_password(password), role)
    def check_password(self, pw: str) -> bool:
        return self.password_hash == _hash_password(pw)

@dataclass
class Patient(User):
    age: int | None = None
    gender: str | None = None
    preferred_speciality: str | None = None
    @classmethod
    def create(cls, name, email, password, age=None, gender=None, pref_spec=None):
        base = User.create(name, email, password, UserRole.PATIENT)
        return cls(**base.__dict__, age=age, gender=gender, preferred_speciality=pref_spec)

@dataclass
class Doctor(User):
    speciality: str = ""
    experience_years: int = 0
    location: str = ""
    consultation_mode: str = "In-person"
    @classmethod
    def create(cls, name, email, password, speciality, exp_yrs=0, location="", mode="In-person"):
        base = User.create(name, email, password, UserRole.DOCTOR)
        return cls(**base.__dict__, speciality=speciality, experience_years=exp_yrs, location=location, consultation_mode=mode)

@dataclass
class TimeSlot:
    slot_id: str
    doctor_id: str
    date: datetime
    start_time: time
    end_time: time
    is_booked: bool = False
    @classmethod
    def create(cls, doctor_id, date, start_time, end_time):
        return cls(str(uuid.uuid4()), doctor_id, date, start_time, end_time)
    def mark_booked(self):
        self.is_booked = True
    def mark_free(self):
        self.is_booked = False

@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    doctor_id: str
    slot_id: str
    status: AppointmentStatus
    created_at: datetime
    @classmethod
    def create(cls, patient_id, doctor_id, slot_id):
        return cls(str(uuid.uuid4()), patient_id, doctor_id, slot_id, AppointmentStatus.BOOKED, datetime.utcnow())
    def cancel(self):
        self.status = AppointmentStatus.CANCELLED
    def complete(self):
        self.status = AppointmentStatus.COMPLETED
