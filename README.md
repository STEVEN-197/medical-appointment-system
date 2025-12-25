# Medical Appointment Scheduling System 🏥

**A Premium OOAD Capstone Project**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-green.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Overview

A full-stack medical appointment scheduling application built with **Object-Oriented Analysis & Design (OOAD)** principles. Features include:

✨ **AI-Powered Recommendations** via Gemini 2.5 Flash  
✨ **Apple-Level UI** with glassmorphism design  
✨ **OOAD Architecture** with clear separation of concerns  
✨ **Secure Authentication** using SHA256 password hashing  
✨ **Real-Time Availability** checks prevent double-booking  
✨ **Natural Language Processing** for appointment requests  

---

## 🏗️ Architecture

```
medical-appointment-system/
├── models/                 # Domain objects (User, Doctor, Patient, Appointment, TimeSlot)
├── services/               # Business logic (Auth, Appointment, AI services)
├── controllers/            # Orchestration layer (AppController)
├── ui/                     # Streamlit UI components & glassmorphism CSS
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── DOCUMENTATION.md       # Complete OOAD documentation
└── UML_DIAGRAMS.md       # PlantUML diagrams (5 types)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Gemini API Key ([Get it here](https://aistudio.google.com))

### Installation

```bash
# Clone repository
git clone https://github.com/STEVEN-197/medical-appointment-system.git
cd medical-appointment-system

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the app
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

---

## 📚 Key Features

### For Patients
- **Registration & Login** with email verification
- **Browse Doctors** by speciality with detailed profiles
- **Book Appointments** with real-time slot availability
- **Manage Appointments** (view, cancel, reschedule)
- **AI Assistant** for natural language appointment requests
- **Appointment History** with status tracking

### For Doctors
- **Secure Login** to access dashboard
- **Define Time Slots** for appointments
- **View Scheduled Appointments**
- **Patient Management** (upcoming appointments)

### For Admin
- **User Management** (view, manage doctors & patients)
- **System Analytics** (usage statistics, audit logs)
- **Doctor Directory** management

---

## 🤖 AI Integration (Gemini 2.5 Flash)

Natural language appointment booking:

```
Patient: "I need a cardiologist next Tuesday morning"
AI: Parses request → Finds best matching doctor + slot
Result: "Dr. Arjun Rao (Cardiologist) - Tuesday 10:00 AM"
```

**AI Capabilities:**
- `parse_natural_query()`: Extracts speciality, urgency, time preferences
- `recommend_slot()`: Suggests optimal appointment based on constraints
- Context-aware: Considers patient history and doctor expertise

---

## 💎 UI Design

**Apple-Inspired Glassmorphism:**
- Dark radial gradient background
- Semi-transparent glass cards with backdrop blur (24px)
- Cyan-to-green gradient buttons with hover animations
- Rounded corners (22px) and premium typography
- High whitespace for readability

```python
with glass_card("Doctor Information"):
    st.write(f"**Dr. {doctor.name}**")
    st.write(f"Speciality: {doctor.speciality}")
    st.write(f"Experience: {doctor.experience_years} years")
```

---

## 📊 OOAD Design Patterns

| Pattern | Usage |
|---------|-------|
| **Inheritance** | User base class → Patient, Doctor, Admin |
| **Encapsulation** | Services hide business logic from UI |
| **Polymorphism** | Different user types, shared authentication interface |
| **Factory** | `User.create()`, `Doctor.create()` for object construction |
| **Service Locator** | AppController centralizes service access |
| **Context Manager** | `with glass_card()` for UI rendering |

---

## 📖 Documentation

- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete academic documentation with OOAD justification
- **[UML_DIAGRAMS.md](UML_DIAGRAMS.md)** - 5 PlantUML diagrams (Use Case, Class, Sequence, Activity, Component)
- **[README.md](README.md)** - This file

---

## 🔐 Security

- ✅ SHA256 password hashing (no plaintext storage)
- ✅ Environment variables for API keys (never hardcoded)
- ✅ Role-based access control (RBAC)
- ✅ Input validation on all forms
- ✅ Session-based authentication in Streamlit

---

## 🚢 Deployment

### Streamlit Cloud (Recommended)

1. Push to GitHub
2. Visit [Streamlit Cloud](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set `GEMINI_API_KEY` in Secrets
5. Deploy (auto-deploys on new commits)

### Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t medibook .
docker run -e GEMINI_API_KEY=<your-key> -p 8501:8501 medibook
```

---

## 📈 Future Roadmap

- [ ] PostgreSQL database integration
- [ ] Email/SMS notifications
- [ ] Payment gateway (Stripe)
- [ ] Video consultations (Zoom API)
- [ ] Analytics dashboard
- [ ] Multi-language support
- [ ] OAuth2 federated login
- [ ] Prescription management
- [ ] Waitlist feature
- [ ] Mobile app

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 👤 Author

**B.E. Bioinformatics Student**  
Satyabhama School of Engineering  
December 2025

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support

For issues or questions:
- Open a GitHub Issue
- Email: [your-email@example.com]
- Check [DOCUMENTATION.md](DOCUMENTATION.md) for detailed info

---

**Made with ❤️ and OOP principles**
