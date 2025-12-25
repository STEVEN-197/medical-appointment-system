import streamlit as st
import os
from datetime import datetime, timedelta
import google.generativeai as genai

# Configure Streamlit page
st.set_page_config(
    page_title="MediBook - Medical Appointment System",
    page_icon="💨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for glassmorphism design
def inject_css():
    st.markdown("""
    <style>
    /* Glassmorphism effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .section-title {
        font-size: 32px;
        font-weight: 600;
        margin: 20px 0 10px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .accent-pill {
        display: inline-block;
        background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.5);
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        font-weight: 600;
        color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

inject_css()

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.user_name = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Setup Gemini AI
try:
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    if api_key:
        genai.configure(api_key=api_key)
        ai_available = True
    else:
        ai_available = False
except:
    ai_available = False

# Sidebar
with st.sidebar:
    st.markdown("### 📄 MediBook")
    st.markdown('<span class="accent-pill">OOAD Capstone</span>', unsafe_allow_html=True)
    st.write("")
    
    if st.session_state.authenticated:
        st.markdown(f"**Logged in as:** {st.session_state.user_name}")
        st.markdown(f"**Role:** {st.session_state.user_role}")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.user_name = None
            st.rerun()
        st.divider()
    
    if not st.session_state.authenticated:
        auth_mode = st.radio("Choose Action", ["Login", "Register"], label_visibility="collapsed")
        
        if auth_mode == "Login":
            st.subheader("🔐 Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Sign In"):
                # Simple demo authentication
                if email and password:
                    st.session_state.authenticated = True
                    st.session_state.user_name = email.split("@")[0].title()
                    st.session_state.user_role = "Doctor" if "doc" in email else "Patient"
                    st.success(f"Welcome, {st.session_state.user_name}!")
                    st.rerun()
                else:
                    st.error("Please enter email and password")
        else:
            st.subheader("✍️ Register")
            name = st.text_input("Full Name", key="reg_name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_password")
            role = st.selectbox("Select Role", ["Patient", "Doctor"], key="reg_role")
            
            if st.button("Create Account"):
                if name and email and password:
                    st.session_state.authenticated = True
                    st.session_state.user_name = name
                    st.session_state.user_role = role
                    st.success(f"Account created! Welcome, {name}!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields")

# Main content
if not st.session_state.authenticated:
    # Welcome page
    st.markdown('<div class="section-title">Welcome to MediBook</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("### Smart medical scheduling, reimagined.")
        st.write("""Book and manage appointments with an Apple‑grade, minimal interface 
        and AI-assisted recommendations. Built as an OOAD capstone project with Streamlit and Gemini AI.""")
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.write("**Quick Start**")
        st.write("📄 Log in or create an account")
        st.write("👨‍⚕️ Browse available doctors")
        st.write("📅 Book your appointment")
        st.write("🤖 Get AI recommendations")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # Authenticated user interface
    if st.session_state.user_role == "Patient":
        page = st.radio("Navigation", ["Browse Doctors", "My Appointments", "AI Assistant"], label_visibility="collapsed")
        
        if page == "Browse Doctors":
            st.markdown('<div class="section-title">Browse Doctors</div>', unsafe_allow_html=True)
            search = st.text_input("Search by speciality (optional)")
            
            # Demo doctors
            doctors = [
                {"name": "Dr. Sarah Johnson", "speciality": "Cardiology", "experience": 12, "location": "New York"},
                {"name": "Dr. Michael Chen", "speciality": "Neurology", "experience": 8, "location": "San Francisco"},
                {"name": "Dr. Emily Rodriguez", "speciality": "Dermatology", "experience": 6, "location": "Los Angeles"},
                {"name": "Dr. James Wilson", "speciality": "Orthopedics", "experience": 15, "location": "Chicago"},
            ]
            
            if search:
                doctors = [d for d in doctors if search.lower() in d["speciality"].lower()]
            
            cols = st.columns(2)
            for idx, doc in enumerate(doctors):
                with cols[idx % 2]:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown(f"**Dr. {doc['name'].split()[-1]}** - {doc['speciality']}")
                    st.write(f"Experience: {doc['experience']} years")
                    st.write(f"Location: {doc['location']}")
                    if st.button(f"Book Appointment", key=f"book_{idx}"):
                        st.session_state.current_page = "booking"
                        st.session_state.selected_doctor = doc
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        
        elif page == "My Appointments":
            st.markdown('<div class="section-title">My Appointments</div>', unsafe_allow_html=True)
            st.info("📌 No appointments yet. Browse doctors to book your first appointment.")
        
        elif page == "AI Assistant":
            st.markdown('<div class="section-title">AI Appointment Assistant</div>', unsafe_allow_html=True)
            
            if not ai_available:
                st.error("⚠️ AI features currently unavailable. Please check configuration.")
            else:
                query = st.text_area("Describe how and when you want to meet a doctor:")
                
                if st.button("Ask MediBook AI"):
                    if query.strip():
                        with st.spinner("Thinking..."):
                            try:
                                model = genai.GenerativeModel('gemini-1.5-flash')
                                response = model.generate_content(
                                    f"""As a medical appointment assistant, analyze this request and provide recommendations:
                                    
                                    Patient request: {query}
                                    
                                    Provide:
                                    1. Recommended speciality
                                    2. Ideal appointment timing
                                    3. Brief reason"""
                                )
                                st.success("🤖 AI Recommendation")
                                st.write(response.text)
                            except Exception as e:
                                st.error(f"AI error: {str(e)}")
                    else:
                        st.warning("Please describe your appointment need.")
    
    elif st.session_state.user_role == "Doctor":
        page = st.radio("Navigation", ["My Schedule", "My Appointments"], label_visibility="collapsed")
        
        if page == "My Schedule":
            st.markdown('<div class="section-title">My Schedule</div>', unsafe_allow_html=True)
            st.info("📅 Schedule feature coming soon.")
        
        elif page == "My Appointments":
            st.markdown('<div class="section-title">My Appointments</div>', unsafe_allow_html=True)
            st.info("📃 No appointments scheduled yet.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 12px;'>
    MediBook © 2024 | OOAD Capstone Project | Built with Streamlit & Gemini AI
</div>
""", unsafe_allow_html=True)
