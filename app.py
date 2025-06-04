import streamlit as st
from predictor import predict_salary
import pandas as pd
import plotly.express as px

st.markdown("""
    <style>
        .main { background-color: #f9f9f9; padding: 20px; }
        .title { color: #2c3e50; text-align: center; }
        .footer { text-align: center; color: gray; font-size: 13px; margin-top: 40px; }
        .stButton>button {
            background-color: #2ecc71;
            color: white;
            border-radius: 5px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='title'>💰 Salary Predictor</h1>", unsafe_allow_html=True)
st.markdown("#Predict your estimated software developer salary based on your background")

st.sidebar.header("Input your information")

# Country options - must match your label encoder's classes exactly!
country = st.sidebar.selectbox("Select your country:" , [
    "United States of America", "India", "Germany", "United Kingdom", "Canada",
    "France", "Australia", "Brazil", "Netherlands", "Poland"
])

# Simpler Education level options for users
edlevel_simple = st.sidebar.selectbox("Select your education level:", [
    "Associate degree",
    "Bachelor's degree",
    "Master's degree",
    "Doctoral degree",
    "Primary school",
    "Professional degree",
    "Secondary school",
    "Some college/university",
    "Other"
])

years_code = st.sidebar.number_input("Years of Coding Experience:" , min_value = 0 , max_value = 50 , value = 3 , step = 1)

# Mapping from your simpler labels to exact labels your model expects
edlevel_map = {
    "Associate degree": "Associate degree (A.A., A.S., etc.)",
    "Bachelor's degree": "Bachelor’s degree (B.A., B.S., B.Eng., etc.)",
    "Master's degree": "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)",
    "Doctoral degree": "Other doctoral degree (Ph.D., Ed.D., etc.)",
    "Primary school": "Primary/elementary school",
    "Professional degree": "Professional degree (JD, MD, etc.)",
    "Secondary school": "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)",
    "Some college/university": "Some college/university study without earning a degree",
    "Other": "Something else"
}

# Map the simple education level to the exact model label
edlevel = edlevel_map[edlevel_simple]

st.markdown("### 📊 Estimated Salary")

col1, col2 = st.columns(2)

with col1:
    if st.button("Predict Salary"):
        try:
            salary = predict_salary(country, edlevel, years_code)
            st.success(f"Predicted Salary: **${salary:,.2f}**")
        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    st.markdown("#### ℹ️ Disclaimer")
    st.info("""
    This prediction is based on historical Stack Overflow developer survey data.
    Salaries can vary widely depending on role, region, and negotiation.
    """)

st.markdown("## 📌 About this Project")
st.write("""
This app predicts the estimated salary of software developers based on their background, 
using data from the Stack Overflow Developer Survey.
""")

st.markdown("## 🧠 How the Model Works")
st.write("""
We trained a machine learning model on cleaned salary data. 
Inputs include country, education level, and years of experience.
""")

st.markdown("## 📂 Data Source")
st.write("""
Data is sourced from the Stack Overflow Developer Survey.
""")

st.markdown("----")
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📊 Salary Insights Dashboard</h2>", unsafe_allow_html=True)
st.markdown("### A visual summary of global software developer salaries based on education, experience, and location.")
df = pd.read_csv("../data/survey_results_public.csv")

df = df.dropna(subset = ["Country", "EdLevel", "YearsCodePro", "ConvertedCompYearly"])

def convert_years(x):
    try:
        return float(x)
    except:
        if "More" in str(x):
            return 51
        elif "Less" in str(x):
            return 0.5
        return None
df["YearsCodePro"] = df["YearsCodePro"].apply(convert_years)

avg_salary_by_country = df.groupby("Country")["ConvertedCompYearly"].mean().sort_values(ascending = False).head(10)
fig_country = px.bar(
    avg_salary_by_country.reset_index(),
    x="Country",
    y="ConvertedCompYearly",
    title="🌍 Top 10 Countries by Average Salary",
    labels={"ConvertedCompYearly": "Average Yearly Salary (USD)"},
    color="ConvertedCompYearly",
    color_continuous_scale="Viridis"
)

avg_salary_by_ed = df.groupby("EdLevel")["ConvertedCompYearly"].mean().sort_values(ascending = False)
fig_ed = px.bar(
    avg_salary_by_ed.reset_index(),
    x = "ConvertedCompYearly",
    y = "EdLevel",
    orientation = "h",
    title = "🎓 Average Salary by Education Level",
    labels = {"ConvertedCompYearly": "Average Yearly Salary (USD)", "EdLevel": "Education Level"},
    color = "ConvertedCompYearly",
    color_continuous_scale = "Blues"
)

# Display first 2 charts side by side
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_country, use_container_width=True)
with col2:
    st.plotly_chart(fig_ed, use_container_width=True)

# Third chart below
avg_salary_by_exp = df.groupby("YearsCodePro")["ConvertedCompYearly"].mean().reset_index()
fig_exp = px.line(
    avg_salary_by_exp,
    x="YearsCodePro",
    y="ConvertedCompYearly",
    title="📈 Salary vs Years of Professional Coding Experience",
    labels={"YearsCodePro": "Years of Experience", "ConvertedCompYearly": "Average Salary (USD)"},
    markers=True
)
st.plotly_chart(fig_exp)

st.markdown("---")
st.markdown("<div class='footer'>Made with ❤️ using <b>Streamlit</b> & <b>Machine Learning</b></div>", unsafe_allow_html=True)
