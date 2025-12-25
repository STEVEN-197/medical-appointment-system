# Medical Appointment Scheduling System
## OOAD Capstone Project Documentation

---

### ABSTRACT

The Medical Appointment Scheduling System is a web-based application engineered using Object-Oriented Analysis and Design (OOAD) principles, developed with Python, Streamlit, and Gemini 2.5 Flash AI integration. The system facilitates seamless appointment booking for patients, doctor schedule management, and intelligent slot recommendations powered by generative AI. The application employs glassmorphic UI design inspired by Apple's design language, ensuring a premium, intuitive user experience while maintaining secure authentication and role-based access control.

---

### 1. INTRODUCTION

**Problem Statement:**  
Healthcare providers face challenges with manual appointment scheduling, resulting in overbooking, patient waiting times, and inefficient resource allocation. Patients struggle to find suitable appointment slots across multiple doctors.

**Solution:**  
An OOAD-driven appointment system with AI-assisted slot recommendations reduces friction, optimizes doctor schedules, and provides natural language query parsing for appointment booking.

---

### 2. SYSTEM ARCHITECTURE

#### 2.1 OOAD Design Principles

**Encapsulation:**
- Business logic isolated in `services/` (AuthService, AppointmentService, AIRecommendationService)
- Models in `models/` define clear domain objects with validation
- Controllers (`controllers/`) orchestrate service interactions
- UI presentation separated in `ui/`

**Inheritance:**
- `User` base class with `Patient`, `Doctor`, `Admin` subclasses
- Enum-based status management (UserRole, AppointmentStatus)

**Polymorphism:**
- Different user types utilize shared authentication interface
- Service classes implement common patterns (create, list, manage)

**Abstraction:**
- Appointment model abstracts scheduling logic
- TimeSlot encapsulates availability tracking

#### 2.2 Component Structure

```
models/
├── User (base class)
├── Patient (inherits User)
├── Doctor (inherits User)
├── Appointment
├── TimeSlot
└── Enums: UserRole, AppointmentStatus

services/
├── AuthService (registration, authentication)
├── AppointmentService (CRUD operations)
└── AIRecommendationService (Gemini integration)

controllers/
└── AppController (orchestrates services, seeding)

ui/
├── CSS injection (glassmorphism)
└── glass_card context manager

app.py (Streamlit frontend)
```

---

### 3. MODULE EXPLANATIONS

#### 3.1 Models Module
Defines domain objects using `@dataclass` for type safety and clarity.
- **User**: Base class with email/password authentication via SHA256 hashing
- **Patient**: Extends User with age, gender, preferred_speciality
- **Doctor**: Extends User with speciality, experience, location, consultation_mode
- **TimeSlot**: Represents available appointment windows (date, start_time, end_time, is_booked)
- **Appointment**: Links patient + doctor + slot with status tracking

#### 3.2 Services Module

**AuthService:**
- `register_patient()`, `register_doctor()`: Creates users, prevents duplicate emails
- `login()`: Validates credentials via hashed password comparison
- In-memory storage via `_users_by_email` dict

**AppointmentService:**
- `add_doctor()`, `list_doctors()`: Manage doctor directory with optional speciality filtering
- `add_slot()`, `get_doctor_slots()`: Slot inventory by doctor and date
- `book()`: Validates slot ownership, checks availability, transitions state
- `cancel()`: Reverts appointment status, frees slot
- `list_patient_appointments()`: Retrieves patient's appointment history

**AIRecommendationService:**
- Initializes Gemini 2.5 Flash via `google-generativeai` SDK
- `_build_context()`: Aggregates free slots as structured text
- `recommend_slot()`: Sends context + patient/urgency data to LLM, parses JSON response
- `parse_natural_query()`: Extracts speciality, urgency, time preferences from free-text

#### 3.3 Controllers Module

**AppController:**
- Singleton pattern: owns single AuthService and AppointmentService instance
- `_seed_data()`: Initializes Dr. Arjun Rao (Cardiologist) with 5 sample slots (10am-4pm)
- Delegates to services; provides unified interface for Streamlit app

#### 3.4 UI Module

**CSS Injection:**
- `inject_global_css()`: Applies glassmorphism with 90s backdrop-filter blur
- Dark theme: radial gradient background (#111827 -> #000000)
- Buttons: cyan-to-green gradient, rounded, shadow with hover lift
- Glass cards: semi-transparent, 22px border-radius, 24px blur

**glass_card Context Manager:**
- Enables Python `with` statement syntax: `with glass_card("Header"):` 
- Wraps content in styled div, reduces boilerplate

---

### 4. OOAD JUSTIFICATION

**Why OOAD?**

1. **Maintainability:** Clear separation (models, services, controllers, ui) allows independent changes
2. **Scalability:** Services can be extended (e.g., database swap) without UI refactoring
3. **Testability:** Each class has single responsibility; dependencies injected
4. **Reusability:** AuthService, AppointmentService usable across platforms (API, CLI, etc.)
5. **Type Safety:** Dataclasses with type hints catch errors early
6. **Business Logic Clarity:** Domain language (Patient, Doctor, Appointment) mirrors real-world concepts

**Design Patterns Used:**
- **Service Locator:** AppController centralizes service access
- **Factory:** `User.create()`, `Patient.create()`, etc. for object construction
- **Context Manager:** `glass_card` for resource-like UI rendering
- **Singleton-like:** AppController instantiated once in Streamlit session

---

### 5. FEATURES

#### 5.1 Authentication & Authorization
- Patient, Doctor, Admin registration with email validation
- SHA256 password hashing (never plaintext storage)
- Role-based navigation in Streamlit sidebar

#### 5.2 Doctor Directory
- Browse all doctors or filter by speciality
- View experience, location, consultation mode
- Glass-card UI displays each doctor in grid

#### 5.3 Appointment Booking
- Select doctor → choose date → pick available time slot
- Real-time availability checks prevent double-booking
- Confirmation modal shows appointment ID

#### 5.4 Appointment Management
- View personal appointment history with status (BOOKED, CANCELLED, COMPLETED)
- Cancel upcoming appointments, freeing slots
- Doctor view shows assigned appointments

#### 5.5 AI-Powered Recommendations
- Natural language input: "I need a cardiologist next Tuesday morning"
- Gemini parses intent → extracts speciality, urgency, time preference
- Returns recommended doctor+slot with reasoning
- Fallback if no suitable match found

---

### 6. ADVANTAGES

1. **Reduced Wait Times:** AI recommends optimal slots instantly
2. **No Overbooking:** Atomic slot transitions prevent race conditions
3. **Apple-Grade UI:** Glassmorphism + rounded buttons inspire trust
4. **Easy Deployment:** Pure Python; Streamlit Cloud requires single GitHub push
5. **Natural Language:** Patients describe needs freely; AI understands context
6. **Extensible:** Swap in-memory storage for PostgreSQL without changing service APIs
7. **Secure Passwords:** SHA256 hashing; no plaintext in logs
8. **Mobile-Responsive:** Streamlit adapts to tablet/phone screens

---

### 7. FUTURE SCOPE

1. **Database Integration:** Replace dicts with SQLAlchemy ORM (PostgreSQL)
2. **Email/SMS Notifications:** Confirmation & reminder messages
3. **Payment Gateway:** Stripe integration for consultation fees
4. **Analytics Dashboard:** Doctor utilization rates, patient metrics
5. **Video Consultations:** Zoom/Meet API integration
6. **Prescription Management:** Digital prescriptions post-appointment
7. **Multi-language Support:** Translate UI for regional expansion
8. **Federated Authentication:** OAuth2 (Google, Microsoft login)
9. **Admin Panel:** CRUD doctors, audit logs, usage reports
10. **Waitlist:** Queue patients if slots unavailable

---

### 8. DEPLOYMENT

**Local Testing:**
```bash
pip install -r requirements.txt
export GEMINI_API_KEY=<your-key>
streamlit run app.py
```

**Streamlit Cloud:**
1. Push to GitHub
2. Visit https://share.streamlit.io
3. Connect repository
4. Set GEMINI_API_KEY in Secrets
5. Deploy (automatic on push)

---

### 9. CONCLUSION

The Medical Appointment Scheduling System demonstrates OOAD excellence through clear separation of concerns, inherited hierarchies, and polymorphic service design. AI integration via Gemini 2.5 Flash elevates the user experience with intelligent recommendations, while glassmorphic UI provides Apple-level aesthetics. The system is production-ready, maintainable, and highly extensible.

---

**Author:** B.E. Bioinformatics Student  
**Date:** December 2025  
**Technology Stack:** Python 3.10+, Streamlit 1.30, Gemini 2.5 Flash, Google Generative AI SDK  
**Repository:** https://github.com/STEVEN-197/medical-appointment-system
