import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("WORKOUT_API_URL", "http://127.0.0.1:8000/workout-plan")

GOALS = ["Build muscle", "Lose fat", "General fitness", "Improve endurance"]
EXPERIENCE = ["Beginner", "Intermediate", "Advanced"]
EQUIPMENT = ["No equipment", "Home dumbbells", "Full gym"]
DAYS_PER_WEEK = list(range(1, 8))

st.set_page_config(page_title="Workout Plan Generator", page_icon="🏋️")
st.title("Workout Plan Generator")
st.write("Tell us about your goals and we'll build a weekly plan for you.")

with st.form("workout_form"):
    goal = st.selectbox("Fitness goal", GOALS)
    experience = st.selectbox("Experience level", EXPERIENCE)
    days_per_week = st.selectbox("Training days per week", DAYS_PER_WEEK, index=2)
    equipment = st.multiselect(
        "Equipment available", EQUIPMENT, default=["No equipment"]
    )
    limitations = st.text_input(
        "Injuries or limitations (optional)",
        placeholder="e.g. bad knees",
        max_chars=300,
    )
    submitted = st.form_submit_button("Generate plan", type="primary")

if submitted:
    if not equipment:
        st.warning("Please select at least one equipment option.")
        st.stop()

    params = {
        "goal": goal,
        "experience": experience,
        "days_per_week": days_per_week,
        "equipment": equipment,  # requests repeats the key for list values
    }
    if limitations.strip():
        params["limitations"] = limitations.strip()

    with st.spinner("Building your plan..."):
        try:
            response = requests.get(API_URL, params=params, timeout=120)
        except requests.RequestException as exc:
            st.error(f"Could not reach the workout API at {API_URL}: {exc}")
            st.stop()

    if response.status_code != 200:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        st.error(f"API error ({response.status_code}): {detail}")
    else:
        st.subheader("Your weekly plan")
        st.markdown(response.json()["plan"])
        if "limitations" in params:
            st.caption(
                "Disclaimer: This plan is not medical advice. Please consult a doctor "
                "or physical therapist before starting, especially with injuries."
            )
