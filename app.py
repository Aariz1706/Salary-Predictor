import streamlit as st
from predictor import predict_salary

# Title
st.title("💰 Salary Predictor")

# Country options - must match your label encoder's classes exactly!
country_options = [
    "United States of America", "India", "Germany", "United Kingdom", "Canada",
    "France", "Australia", "Brazil", "Netherlands", "Poland"
]

# Simpler Education level options for users
edlevel_options = [
    "Associate degree",
    "Bachelor's degree",
    "Master's degree",
    "Doctoral degree",
    "Professional degree",
    "Secondary school",
    "Some college/university",
    "Other"
]

# Mapping from your simpler labels to exact labels your model expects
edlevel_map = {
    "Associate degree": "Associate degree (A.A., A.S., etc.)",
    "Bachelor's degree": "Bachelor’s degree (B.A., B.S., B.Eng., etc.)",
    "Master's degree": "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)",
    "Doctoral degree": "Other doctoral degree (Ph.D., Ed.D., etc.)",
    "Professional degree": "Professional degree (JD, MD, etc.)",
    "Secondary school": "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)",
    "Some college/university": "Some college/university study without earning a degree",
    "Other": "Something else"
}

# User inputs
country = st.selectbox("Select your country:", country_options)
edlevel_simple = st.selectbox("Select your education level:", edlevel_options)
years_code = st.number_input("Years of coding experience:", min_value=0, max_value=50, value=3, step=1)

# Map the simple education level to the exact model label
edlevel = edlevel_map[edlevel_simple]

# Predict button
if st.button("Predict Salary"):
    salary = predict_salary(country, edlevel, years_code)
    st.success(f"Predicted Salary: ${salary:,.2f}")
