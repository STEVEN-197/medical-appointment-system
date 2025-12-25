import streamlit as st
import os
from datetime import datetime
import google.generativeai as genai

st.set_page_config(page_title="MediBook", page_icon="💨", layout="wide", initial_sidebar_state="expanded")

def inject_css():
    st.markdown("""
    <style>
    .glass-card {
        background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 16px;
        padding: 20px; margin: 10px 0; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    .section-title {
        font-size: 32px; font-weight: 600; margin: 20px 0 10px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .accent-pill { display: inline-block; background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.5); border-radius: 20px;
        padding: 4px 12px; font-size: 12px; font-weight: 600; color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_name = None
    st.session_state.booking_mode = False
    st.session_state.selected_doc = None

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
if api_key:
    genai.configure(api_key=api_key)
    ai_available = True
else:
    ai_available = False

with st.sidebar:
    st.markdown("### 📄 MediBook")
    st.markdown('<span class="accent-pill">OOAD Capstone</span>', unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        st.markdown(f"**Logged in as:** {st.session_state.user_name}")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.booking_mode = False
            st.rerun()
        st.divider()
    
    if not st.session_state.authenticated:
        auth_tab = st.radio("Choose Action", ["Login", "Register"], label_visibility="collapsed")
        
        if auth_tab == "Login":
            st.subheader("🔐 Login")
            email = st.text_input("Email", key="login_email")
            pwd = st.text_input("Password", type="password", key="login_pwd")
            if st.button("Sign In", use_container_width=True):
                if email and pwd:
                    st.session_state.authenticated = True
                    st.session_state.user_name = email.split("@")[0].title()
                    st.session_state.user_role = "Patient"
                    st.success(f"Welcome, {st.session_state.user_name}!")
                    st.rerun()
                else:
                    st.error("Enter email and password")
        else:
            st.subheader("✍️ Register")
            name = st.text_input("Full Name", key="reg_name")
            email = st.text_input("Email", key="reg_email")
            pwd = st.text_input("Password", type="password", key="reg_pwd")
            if st.button("Create Account", use_container_width=True):
                if name and email and pwd:
                    st.session_state.authenticated = True
                    st.session_state.user_name = name
                    st.session_state.user_role = "Patient"
                    st.success(f"Account created! Welcome, {name}!")
                    st.rerun()
                else:
                    st.error("Fill all fields")

doctors_list = [
    {"id": 1, "name": "Dr. Sarah Johnson", "spec": "Cardiology", "exp": 12, "loc": "New York"},
    {"id": 2, "name": "Dr. Michael Chen", "spec": "Neurology", "exp": 8, "loc": "San Francisco"},
    {"id": 3, "name": "Dr. Emily Rodriguez", "spec": "Dermatology", "exp": 6, "loc": "Los Angeles"},
    {"id": 4, "name": "Dr. James Wilson", "spec": "Orthopedics", "exp": 15, "loc": "Chicago"},
    {"id": 5, "name": "Dr. Lisa Anderson", "spec": "Pediatrics", "exp": 10, "loc": "Houston"},
    {"id": 6, "name": "Dr. Robert Kumar", "spec": "Oncology", "exp": 20, "loc": "Boston"},
    {"id": 7, "name": "Dr. Jessica Lee", "spec": "Pulmonology", "exp": 9, "loc": "Seattle"},
    {"id": 8, "name": "Dr. David Martinez", "spec": "Gastroenterology", "exp": 14, "loc": "Miami"},
    {"id": 9, "name": "Dr. Priya Patel", "spec": "Psychiatry", "exp": 11, "loc": "Denver"},
    {"id": 10, "name": "Dr. Christopher Brown", "spec": "Ophthalmology", "exp": 7, "loc": "Austin"},
    {"id": 11, "name": "Dr. Amanda White", "spec": "Endocrinology", "exp": 13, "loc": "Philadelphia"},
    {"id": 12, "name": "Dr. Thomas Garcia", "spec": "Urology", "exp": 18, "loc": "Dallas"},
    {"id": 13, "name": "Dr. Victoria Lee", "spec": "Rheumatology", "exp": 9, "loc": "Portland"},
    {"id": 14, "name": "Dr. William Harris", "spec": "Nephrology", "exp": 12, "loc": "Atlanta"},
    {"id": 15, "name": "Dr. Sophie Clark", "spec": "Hematology", "exp": 10, "loc": "Phoenix"},
]

if not st.session_state.authenticated:
    st.markdown('<div class="section-title">Welcome to MediBook</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("### Smart medical scheduling, reimagined.")
        st.write("Book appointments with AI-assisted recommendations.")
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("**Features**")
        st.write("📄 Register/Login")
        st.write("👨‍⚕️ Browse 15+ Doctors")
        st.write("📅 Book Appointments")
        st.write("🤖 AI Recommendations")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.booking_mode and st.session_state.selected_doc:
    doc = st.session_state.selected_doc
    st.markdown(f'<div class="section-title">Book Appointment with Dr. {doc["name"].split()[-1]}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        book_date = st.date_input("Select Date", min_value=datetime.now().date())
    with col2:
        book_time = st.selectbox("Select Time", ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Confirm Booking", use_container_width=True):
            st.success(f"Appointment booked! Dr. {doc['name']} on {book_date} at {book_time}")
            st.session_state.booking_mode = False
            st.session_state.selected_doc = None
            st.rerun()
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.booking_mode = False
            st.session_state.selected_doc = None
            st.rerun()

else:
    page = st.radio("Navigation", ["Browse Doctors", "My Appointments", "AI Assistant"], label_visibility="collapsed")
    
    if page == "Browse Doctors":
        st.markdown('<div class="section-title">Browse Doctors</div>', unsafe_allow_html=True)
        search_spec = st.text_input("Search by speciality")
        filtered = [d for d in doctors_list if not search_spec or search_spec.lower() in d["spec"].lower()]
        
        if not filtered:
            st.info("No doctors found")
        else:
            cols = st.columns(2)
            for idx, doc in enumerate(filtered):
                with cols[idx % 2]:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown(f"**Dr. {doc['name'].split()[-1]}** - {doc['spec']}")
                    st.write(f"Experience: {doc['exp']} years | Location: {doc['loc']}")
                    if st.button(f"Book Now", key=f"book_{doc['id']}", use_container_width=True):
                        st.session_state.selected_doc = doc
                        st.session_state.booking_mode = True
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
    
    elif page == "My Appointments":
        st.markdown('<div class="section-title">My Appointments</div>', unsafe_allow_html=True)
        st.info("📌 No appointments yet. Book one from Browse Doctors!")
    
    elif page == "AI Assistant":
        st.markdown('<div class="section-title">AI Assistant</div>', unsafe_allow_html=True)
        if not ai_available:
            st.error("⚠️ API Key not configured")
        else:
            query = st.text_area("Describe your appointment need:")
            if st.button("Ask AI", use_container_width=True):
                if query.strip():
                    with st.spinner("Processing..."):
                        try:
                            model = genai.GenerativeModel('gemini-2.5-flash')
                            response = model.generate_content(f"Medical appointment assistant. Patient request: {query}. Provide: 1) Recommended speciality 2) Urgency level 3) Brief suggestion")
                            st.success("🤖 AI Recommendation")
                            st.write(response.text)
                        except Exception as e:
                            st.error(f"API Error: {str(e)[:100]}")
                else:
                    st.warning("Please describe your appointment need")

st.divider()
st.markdown("<div style='text-align:center;color:#999;font-size:12px;'>MediBook © 2024 | Built with Streamlit & Gemini AI</div>", unsafe_allow_html=True)
