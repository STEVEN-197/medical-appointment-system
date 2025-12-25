# UML Diagrams - Medical Appointment Scheduling System

## 1. USE CASE DIAGRAM

```plantuml
@startuml
left to right direction
skinparam usecase {
  BackgroundColor #F4F4F6
  BorderColor #555555
}
skinparam actor {
  BackgroundColor #E8F4F8
}

rectangle "Medical Appointment System" {
  usecase "Register" as UC_Register
  usecase "Login" as UC_Login
  usecase "Browse Doctors" as UC_Browse
  usecase "Search by Speciality" as UC_Search
  usecase "View Doctor Profile" as UC_ViewDoc
  usecase "Book Appointment" as UC_Book
  usecase "Check Availability" as UC_CheckSlot
  usecase "Cancel Appointment" as UC_Cancel
  usecase "View My Appointments" as UC_ViewAppts
  usecase "Manage Slots" as UC_ManageSlots
  usecase "AI Recommendation" as UC_AiSlot
  usecase "Parse Natural Language" as UC_NLRequest
}

actor Patient
actor Doctor
actor Admin

Patient -- UC_Register
Patient -- UC_Login
Patient -- UC_Browse
Patient -- UC_Search
Patient -- UC_ViewDoc
Patient -- UC_Book
Patient -- UC_CheckSlot
Patient -- UC_Cancel
Patient -- UC_ViewAppts
Patient -- UC_AiSlot
Patient -- UC_NLRequest

Doctor -- UC_Login
Doctor -- UC_ManageSlots
Doctor -- UC_ViewAppts

Admin -- UC_Login

UC_Book .> UC_CheckSlot : <<include>>
UC_AiSlot .> UC_CheckSlot : <<include>>
UC_NLRequest .> UC_AiSlot : <<include>>
UC_Cancel .> UC_ViewAppts : <<extend>>

@enduml
```

---

## 2. CLASS DIAGRAM

```plantuml
@startuml
skinparam class {
  BackgroundColor #F7F7FA
  BorderColor #555555
}

class User {
  - id: str
  - name: str
  - email: str
  - password_hash: str
  - role: UserRole
  + check_password(pw: str): bool
  + {static} create(name, email, pwd, role): User
}

class Patient {
  - age: int | None
  - gender: str | None
  - preferred_speciality: str | None
  + {static} create(...): Patient
}

class Doctor {
  - speciality: str
  - experience_years: int
  - location: str
  - consultation_mode: str
  + {static} create(...): Doctor
}

class Admin {
  + manage_doctors(): void
  + manage_users(): void
}

class TimeSlot {
  - slot_id: str
  - doctor_id: str
  - date: datetime
  - start_time: time
  - end_time: time
  - is_booked: bool
  + mark_booked(): void
  + mark_free(): void
  + {static} create(...): TimeSlot
}

class Appointment {
  - appointment_id: str
  - patient_id: str
  - doctor_id: str
  - slot_id: str
  - status: AppointmentStatus
  - created_at: datetime
  + cancel(): void
  + complete(): void
  + {static} create(...): Appointment
}

class AuthService {
  - _users_by_email: Dict[str, User]
  + register_patient(...): Patient
  + register_doctor(...): Doctor
  + login(email, password): User | None
}

class AppointmentService {
  - doctors: Dict[str, Doctor]
  - slots: Dict[str, TimeSlot]
  - appointments: Dict[str, Appointment]
  + add_doctor(doctor): void
  + list_doctors(speciality): list[Doctor]
  + add_slot(slot): void
  + get_doctor_slots(doctor_id, date): list[TimeSlot]
  + book(patient, doctor, slot_id): Appointment
  + cancel(appointment_id, patient): void
  + list_patient_appointments(patient): list[Appointment]
}

class AIRecommendationService {
  - model_name: str
  - appointment_service: AppointmentService
  + recommend_slot(patient, speciality, urgency, constraints): Dict
  + parse_natural_query(text): Dict
  - _build_context(speciality): str
}

class AppController {
  - auth: AuthService
  - appt_service: AppointmentService
  + login(email, password): User | None
  + register_patient(...): Patient
  + get_doctors(speciality): list[Doctor]
  + get_doctor_slots(...): list[TimeSlot]
  + book_appointment(patient, doctor, slot_id): Appointment
  + cancel_appointment(patient, appointment_id): void
  + get_patient_appointments(patient): list[Appointment]
}

User <|-- Patient
User <|-- Doctor
User <|-- Admin

Doctor "1" o-- "*" TimeSlot
Patient "1" o-- "*" Appointment
Doctor "1" o-- "*" Appointment
TimeSlot "1" -- "0..1" Appointment : books

AppointmentService --> Doctor
AppointmentService --> TimeSlot
AppointmentService --> Appointment
AuthService --> User
AuthService --> Patient
AuthService --> Doctor

AIRecommendationService --> AppointmentService
AppController --> AuthService
AppController --> AppointmentService
AppController --> AIRecommendationService

@enduml
```

---

## 3. SEQUENCE DIAGRAM (Book Appointment)

```plantuml
@startuml
actor Patient
participant "Streamlit UI" as UI
control "AppController" as C
control "AppointmentService" as S
entity "TimeSlot" as Slot
entity "Appointment" as Appt

Patient -> UI: Select doctor, date, timeSlot
UI -> C: book_appointment(doctor_id, slot_id)
C -> S: get_slot(doctor_id, slot_id)
S -> Slot: check is_booked
Slot --> S: is_booked = false
S -> Appt: create(patient_id, doctor_id, slot_id)
Appt --> S: appointment_instance
S -> Slot: mark_booked()
S --> C: appointment_instance
C --> UI: booking_success(appointment)
UI --> Patient: show confirmation + ID

@enduml
```

---

## 4. ACTIVITY DIAGRAM (Appointment Booking Workflow)

```plantuml
@startuml
start
:Patient logs in;
:Navigate to Browse Doctors;
:Search/filter by speciality;
:View doctor details;
:Select doctor;
:Choose appointment date;
if (Any free slots on date?) then (yes)
  :Display available time slots;
  :Patient selects time slot;
  if (Slot still available?) then (yes)
    :Create Appointment record;
    :Update TimeSlot (mark booked);
    :Show confirmation;
    :Notify patient;
  else (no)
    :Show error "Slot taken";
  endif
else (no)
  :Show "No availability";
  :Suggest AI recommendation;
endif
stop

@enduml
```

---

## 5. AI FLOW DIAGRAM

```plantuml
@startuml
start
:Patient enters natural language request;
if (Gemini API configured?) then (yes)
  :Send query to Gemini 2.5 Flash;
  :Parse AI response (JSON);
  :Extract speciality, urgency, constraints;
  :Build free slot context from database;
  :Send context + preferences to Gemini;
  :Get recommendation JSON;
  if (Valid recommendation?) then (yes)
    :Show recommended doctor + slot;
    :Option to confirm booking;
  else (no)
    :Show "No suitable match";
  endif
else (no)
  :Show configuration error;
  :Suggest adding API key;
endif
stop

@enduml
```

---

## 6. COMPONENT DIAGRAM

```plantuml
@startuml
package "Presentation" {
  component "Streamlit App" as App
  component "Glass Card UI" as UI
}

package "Controllers" {
  component "AppController" as AC
}

package "Services" {
  component "AuthService" as Auth
  component "AppointmentService" as Appt
  component "AIRecommendationService" as AI
}

package "Models" {
  component "Domain Objects" as Models
}

package "External" {
  component "Gemini API" as Gemini
}

App --> AC
UI --> App
AC --> Auth
AC --> Appt
AC --> AI
Appt --> Models
Auth --> Models
AI --> Gemini
AI --> Appt

@enduml
```

---

## How to View Diagrams

1. Copy PlantUML code above
2. Visit https://www.plantuml.com/plantuml/uml/
3. Paste code in editor
4. View rendered diagram
5. Export as PNG/SVG

**Alternative:** Use VSCode extension "PlantUML" for live preview
