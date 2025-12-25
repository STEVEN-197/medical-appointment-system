import streamlit as st
import os
from datetime import datetime, time, timedelta
from controllers.app_controller import AppController
from ui.layout import inject_global_css, glass_card
from services.ai_service import AIRecommendationService
from models.user import UserRole

st.set_page_config(
    page_title="MediBook · Medical Appointment System",
    page_icon="\ud83d\udca8",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_global_css()

if "controller" not in st.session_state:
    st.session_state.controller = AppController()

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "ai_service" not in st.session_state:
    try:
        st.session_state.ai_service = AIRecommendationService(st.session_state.controller.appt_service)
        st.session_state.ai_error = None
    except RuntimeError as e:
        st.session_state.ai_service = None
        st.session_state.ai_error = str(e)

controller = st.session_state.controller

with st.sidebar:
    st.markdown("### \ud83d\udcc4 MediBook")
    st.markdown('<span class="accent-pill">OOAD Capstone</span>', unsafe_allow_html=True)
    st.write("\n")
    
    if st.session_state.current_user:
        st.markdown(f"**Logged in as:** {st.session_state.current_user.name}")
        st.markdown(f"**Role:** {st.session_state.current_user.role.value}")
        if st.button("\ud83d\udeaa Logout"):
            st.session_state.current_user = None
            st.rerun()
        st.divider()
    
    if not st.session_state.current_user:
        auth_mode = st.radio("Choose Action", ["Login", "Register"], label_visibility="collapsed")
        if auth_mode == "Login":
            st.subheader("Login")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Sign In"):
                user = controller.login(login_email, login_password)
                if user:
                    st.session_state.current_user = user
                    st.success(f"Welcome, {user.name}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password")
        else:
            st.subheader("Register")
            reg_name = st.text_input("Name", key="reg_name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_role = st.selectbox("Role", ["Patient", "Doctor"], key="reg_role")
            
            if reg_role == "Doctor":
                reg_speciality = st.text_input("Speciality", key="reg_speciality")
                reg_exp = st.number_input("Years of Experience", min_value=0, max_value=50, key="reg_exp")
                reg_loc = st.text_input("Location", key="reg_loc")
            else:
                reg_age = st.number_input("Age", min_value=0, max_value=120, key="reg_age")
                reg_gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="reg_gender")
                reg_speciality_pref = st.text_input("Preferred Speciality (optional)", key="reg_spec_pref")
            
            if st.button("Create Account"):
                try:
                    if reg_role == "Doctor":
                        user = controller.auth.register_doctor(
                            reg_name, reg_email, reg_password,
                            speciality=reg_speciality, experience_years=reg_exp, location=reg_loc
                        )
                        controller.appt_service.add_doctor(user)
                    else:
                        user = controller.register_patient(
                            reg_name, reg_email, reg_password,
                            age=reg_age, gender=reg_gender, preferred_speciality=reg_speciality_pref
                        )
                    st.session_state.current_user = user
                    st.success(f"Account created! Welcome, {user.name}!")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
    else:
        if st.session_state.current_user.role == UserRole.PATIENT:
            page = st.radio("Navigation", ["Browse Doctors", "My Appointments", "AI Assistant"], label_visibility="collapsed")
        elif st.session_state.current_user.role == UserRole.DOCTOR:
            page = st.radio("Navigation", ["My Schedule", "My Appointments"], label_visibility="collapsed")
        else:
            page = st.radio("Navigation", ["Manage System"], label_visibility="collapsed")

if not st.session_state.current_user:
    st.markdown('<div class="section-title">Welcome to MediBook</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("###  Smart medical scheduling, reimagined.")
        st.write("Book and manage appointments with an Apple\u2011grade, minimal interface and AI-assisted recommendations.")
    with col2:
        with glass_card("Quick Start"):
            st.write("\ud83d\udcc4 Log in or create an account")
            st.write("\ud83d\udc68\u200d\u2695\ufe0f Browse available doctors")
            st.write("\ud83d\udcc5 Book your appointment")
            st.write("\ud83e\udd16 Get AI recommendations")
else:
    page = st.session_state.get("current_page", "Browse Doctors" if st.session_state.current_user.role == UserRole.PATIENT else "My Schedule")
    
    if st.session_state.current_user.role == UserRole.PATIENT:
        if "page" in locals() and page == "Browse Doctors":
            st.markdown('<div class="section-title">Browse Doctors</div>', unsafe_allow_html=True)
            search_speciality = st.text_input("Search by Speciality (optional)")
            doctors = controller.get_doctors(search_speciality if search_speciality else None)
            
            if not doctors:
                st.info("No doctors found matching your criteria.")
            else:
                cols = st.columns(2)
                for idx, doc in enumerate(doctors):
                    with cols[idx % 2]:
                        with glass_card(doc.speciality):
                            st.markdown(f"**Dr. {doc.name}**")
                            st.write(f"Experience: {doc.experience_years} years")
                            st.write(f"Location: {doc.location}")
                            st.write(f"Mode: {doc.consultation_mode}")
                            if st.button(f"Book Appointment", key=f"book_{doc.id}"):
                                st.session_state.selected_doctor = doc
                                st.session_state.current_page = "booking"
                                st.rerun()
        
        elif st.session_state.get("current_page") == "booking" and "selected_doctor" in st.session_state:
            doctor = st.session_state.selected_doctor
            st.markdown(f'<div class="section-title">Book with Dr. {doctor.name}</div>', unsafe_allow_html=True)
            
            book_date = st.date_input("Select Date", min_value=datetime.now().date())
            slots = controller.get_doctor_slots(doctor.id, datetime.combine(book_date, time()))
            available_slots = [s for s in slots if not s.is_booked]
            
            if not available_slots:
                st.warning("No available slots on this date.")
            else:
                slot_options = {f"{s.start_time} - {s.end_time}": s.slot_id for s in available_slots}
                selected_slot_str = st.selectbox("Select Time", list(slot_options.keys()))
                selected_slot_id = slot_options[selected_slot_str]
                
                if st.button("Confirm Booking"):
                    try:
                        appt = controller.book_appointment(
                            st.session_state.current_user, doctor, selected_slot_id
                        )
                        st.success(f"Appointment booked! ID: {appt.appointment_id}")
                        del st.session_state.selected_doctor
                        del st.session_state.current_page
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
        
        elif "page" in locals() and page == "My Appointments":
            st.markdown('<div class="section-title">My Appointments</div>', unsafe_allow_html=True)
            appts = controller.get_patient_appointments(st.session_state.current_user)
            if not appts:
                st.info("No appointments yet.")
            else:
                for appt in appts:
                    with glass_card(appt.status.value):
                        slot = controller.appt_service.slots.get(appt.slot_id)
                        doctor = controller.appt_service.doctors.get(appt.doctor_id)
                        if slot and doctor:
                            st.write(f"**Doctor:** Dr. {doctor.name}")
                            st.write(f"**Date & Time:** {slot.date.date()} {slot.start_time}")
                            st.write(f"**Status:** {appt.status.value}")
                            if appt.status.value == "BOOKED" and st.button(f"Cancel", key=f"cancel_{appt.appointment_id}"):
                                controller.cancel_appointment(st.session_state.current_user, appt.appointment_id)
                                st.success("Appointment cancelled.")
                                st.rerun()
        
        elif "page" in locals() and page == "AI Assistant":
            st.markdown('<div class="section-title">AI Appointment Assistant</div>', unsafe_allow_html=True)
            if st.session_state.ai_service is None:
                st.error(f"AI not configured: {st.session_state.ai_error}")
            else:
                query = st.text_area("Describe how and when you want to meet a doctor:")
                if st.button("Ask MediBook AI"):
                    if query.strip():
                        parsed = st.session_state.ai_service.parse_natural_query(query)
                        speciality = parsed.get("speciality") or st.session_state.current_user.preferred_speciality
                        result = st.session_state.ai_service.recommend_slot(
                            patient=st.session_state.current_user,
                            speciality=speciality,
                            urgency=parsed.get("urgency") or "normal",
                            constraints=parsed,
                        )
                        if result:
                            st.success(f"AI Recommendation: {result.get('reason', 'Suggested slot found.')}")
                            st.info(f"Doctor ID: {result.get('doctor_id')}\nSlot ID: {result.get('slot_id')}")
                        else:
                            st.error("AI could not find a suitable slot.")
                    else:
                        st.warning("Please describe your appointment need.")
