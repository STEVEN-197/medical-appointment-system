import streamlit as st
import os
from datetime import datetime
import google.generativeai as genai

st.set_page_config(page_title="MediBook", page_icon="💨", layout="wide")

def inject_css():
    st.markdown("""
    <style>
    .glass-card {background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); border-radius: 16px; padding: 20px; margin: 10px 0; box-shadow: 0 8px 32px rgba(0,0,0,0.1);}
    .section-title {font-size: 32px; font-weight: 600; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;}
    .accent-pill {display: inline-block; background: rgba(102, 126, 234, 0.2); border: 1px solid rgba(102, 126, 234, 0.5); border-radius: 20px; padding: 4px 12px; font-size: 12px; font-weight: 600; color: #667eea;}
    </style>
    """, unsafe_allow_html=True)

inject_css()

if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = None
    st.session_state.booking = False
    st.session_state.doc_sel = None

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
if api_key:
    genai.configure(api_key=api_key)
    ai_ok = True
else:
    ai_ok = False

docs = [
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

with st.sidebar:
    st.markdown("### 📄 MediBook")
    st.markdown('<span class="accent-pill">OOAD Capstone</span>', unsafe_allow_html=True)
    if st.session_state.auth:
        st.markdown(f"**{st.session_state.user}**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth = False
            st.session_state.booking = False
            st.rerun()
    else:
        tab = st.radio("Action", ["Login", "Register"], label_visibility="collapsed")
        if tab == "Login":
            st.subheader("🔐 Login")
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            if st.button("Sign In", use_container_width=True):
                if e and p:
                    st.session_state.auth = True
                    st.session_state.user = e.split("@")[0]
                    st.success("Logged in!")
                    st.rerun()
        else:
            st.subheader("✍️ Register")
            n = st.text_input("Name")
            e = st.text_input("Email")
            p = st.text_input("Password", type="password")
            if st.button("Create", use_container_width=True):
                if n and e and p:
                    st.session_state.auth = True
                    st.session_state.user = n
                    st.success("Account created!")
                    st.rerun()

if not st.session_state.auth:
    st.markdown('<div class="section-title">Welcome to MediBook</div>', unsafe_allow_html=True)
    st.write("### Smart medical scheduling, reimagined.")
    st.write("Book appointments with AI-assisted recommendations.")
else:
    if st.session_state.booking and st.session_state.doc_sel:
        doc = st.session_state.doc_sel
        st.markdown(f'<div class="section-title">Book with Dr. {doc["name"].split()[-1]}</div>', unsafe_allow_html=True)
        d = st.date_input("Date", min_value=datetime.now().date())
        t = st.selectbox("Time", ["09:00 AM", "10:00 AM", "11:00 AM", "02:00 PM", "03:00 PM", "04:00 PM"])
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Confirm", use_container_width=True):
                st.success(f"Booked! Dr. {doc['name']} on {d} at {t}")
                st.session_state.booking = False
                st.rerun()
        with c2:
            if st.button("❌ Back", use_container_width=True):
                st.session_state.booking = False
                st.rerun()
    else:
        page = st.radio("Menu", ["Doctors", "Appointments", "AI"], label_visibility="collapsed")
        if page == "Doctors":
            st.markdown('<div class="section-title">Browse Doctors</div>', unsafe_allow_html=True)
            search = st.text_input("Search")
            flt = [d for d in docs if not search or search.lower() in d["spec"].lower()]
            cols = st.columns(2)
            for i, d in enumerate(flt):
                with cols[i % 2]:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown(f"**Dr. {d['name'].split()[-1]}** - {d['spec']}")
                    st.write(f"{d['exp']}y | {d['loc']}")
                    if st.button("Book", key=f"b{d['id']}", use_container_width=True):
                        st.session_state.doc_sel = d
                        st.session_state.booking = True
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        elif page == "Appointments":
            st.markdown('<div class="section-title">Appointments</div>', unsafe_allow_html=True)
            st.info("📌 No appointments yet")
        else:
            st.markdown('<div class="section-title">AI Assistant</div>', unsafe_allow_html=True)
            if not ai_ok:
                st.error("API not configured")
            else:
                q = st.text_area("Need help?")
                if st.button("Ask AI", use_container_width=True):
                    if q.strip():
                        with st.spinner("Processing..."):
                            try:
                                m = genai.GenerativeModel('gemini-2.5-flash')
                                r = m.generate_content(f"Medical assistant. Request: {q}. Provide: 1)Speciality 2)Urgency 3)Suggestion")
                                st.success("🤖 Recommendation")
                                st.write(r.text)
                            except Exception as e:
                                st.error(f"Error: {str(e)[:80]}")

st.divider()
st.markdown("<div style='text-align:center;color:#999;font-size:11px;'>MediBook © 2024 | Streamlit + Gemini</div>", unsafe_allow_html=True)
