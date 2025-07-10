<<<<<<< HEAD
import streamlit as st
from predictor import predict_salary
import sqlite3
import pandas as pd
import plotly.express as px

# Database setup
conn = sqlite3.connect("users.db") #Opens or creates a file named users.db to store data.("users.db")
cursor = conn.cursor() #Creates a cursor object which is used to execute SQL commands.

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""") #Creates a table named users if it doesn't exist yet , ensures each username is unique and stroes the password in plain text
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    username TEXT,
    country TEXT,
    education TEXT,
    experience INTEGER,
    predicted_salary TEXT)
    """)
conn.commit()

# User Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    auth_choice = st.radio("Select Option", ["Login", "Sign Up"])

    if auth_choice == "Sign Up":
        st.subheader("Create a New Account")
        new_user = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Sign Up"):
            cursor.execute("SELECT * FROM users WHERE username=?", (new_user,))
            if cursor.fetchone():
                st.warning("Username already exists.")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_user, new_password))
                conn.commit()
                st.success("Account created! Please log in.")

    elif auth_choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if cursor.fetchone():
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    st.stop()

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
st.markdown("<h3>Predict your estimated software developer salary based on your background</h3>")

st.sidebar.header("Input your information") 

# Country options - must match your label encoder's classes exactly!
country = st.sidebar.selectbox("Select your country:" , [
    "United States of America", "India", "Germany", "Canada",
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


role = st.sidebar.selectbox("Developer Role:", [
    "Developer, back-end", "Developer, front-end", "Developer, full-stack",
    "Developer, mobile", "Data scientist or machine learning specialist",
    "Engineer, data", "DevOps specialist", "System administrator", "Designer"
    ])

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()


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
            salary = predict_salary(country, edlevel, years_code, role)
            st.success(f"Predicted Salary: **${salary:,.2f}**")

            # # Save to session_state history
            # if "prediction_history" not in st.session_state:
            #     st.session_state.prediction_history = []

            # st.session_state.prediction_history.append({
            #     "User": st.session_state.username,
            #     "Country": country,
            #     "Education": edlevel,
            #     "Experience": years_code,
            #     "Predicted Salary": f"${salary:,.2f}"
            # })
            # Save prediction to SQLite DB
            cursor.execute("""
                INSERT INTO history (username, country, education, experience, predicted_salary)
                VALUES (?, ?, ?, ?, ?)
            """, (st.session_state.username, country, edlevel, years_code, f"${salary:,.2f}"))
            conn.commit()


        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    st.markdown("#### ℹ️ Disclaimer")
    st.info("""
    This prediction is based on historical Stack Overflow developer survey data.
    Salaries can vary widely depending on role, region, and negotiation.
    """)

st.markdown("### 📁 Prediction History")
# Fetch history from DB
cursor.execute("SELECT country, education, experience, predicted_salary FROM history WHERE username=?", (st.session_state.username,))
records = cursor.fetchall()

if records:
    history_df = pd.DataFrame(records, columns=["Country", "Education", "Experience", "Predicted Salary"])
    st.table(history_df)

    csv = history_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download History as CSV",
        data=csv,
        file_name='salary_predictions.csv',
        mime='text/csv')
else:
    st.info("No predictions yet.")



st.markdown("## 📌 About this Project")
st.write("""
This app predicts the estimated salary of software developers based on their background, 
using data from the Stack Overflow Developer Survey.
""")

st.markdown("## 🧠 How the Model Works")
st.write("""
We trained a machine learning model on cleaned salary data. 
Inputs include country, education level, years of experience and roles.
""")

st.markdown("## 📂 Data Source")
st.write("""
Data is sourced from the Stack Overflow Developer Survey.
""")

st.markdown("----")
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📊 Salary Insights Dashboard</h2>", unsafe_allow_html=True)
st.markdown("### A visual summary of global software developer salaries based on education, roles, experience, and location.")
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
=======
import streamlit as st
from predictor import predict_salary
import sqlite3
import pandas as pd
import plotly.express as px

# Database setup
conn = sqlite3.connect("users.db") #Opens or creates a file named users.db to store data.("users.db")
cursor = conn.cursor() #Creates a cursor object which is used to execute SQL commands.

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""") #Creates a table named users if it doesn't exist yet , ensures each username is unique and stroes the password in plain text
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    username TEXT,
    country TEXT,
    education TEXT,
    experience INTEGER,
    predicted_salary TEXT)
    """)
conn.commit()

# User Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    auth_choice = st.radio("Select Option", ["Login", "Sign Up"])

    if auth_choice == "Sign Up":
        st.subheader("Create a New Account")
        new_user = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Sign Up"):
            cursor.execute("SELECT * FROM users WHERE username=?", (new_user,))
            if cursor.fetchone():
                st.warning("Username already exists.")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_user, new_password))
                conn.commit()
                st.success("Account created! Please log in.")

    elif auth_choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if cursor.fetchone():
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    st.stop()

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
st.markdown("<h3>Predict your estimated software developer salary based on your background</h3>")

st.sidebar.header("Input your information") 

# Country options - must match your label encoder's classes exactly!
country = st.sidebar.selectbox("Select your country:" , [
    "United States of America", "India", "Germany", "Canada",
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


role = st.sidebar.selectbox("Developer Role:", [
    "Developer, back-end", "Developer, front-end", "Developer, full-stack",
    "Developer, mobile", "Data scientist or machine learning specialist",
    "Engineer, data", "DevOps specialist", "System administrator", "Designer"
    ])

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()


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
            salary = predict_salary(country, edlevel, years_code, role)
            st.success(f"Predicted Salary: **${salary:,.2f}**")

            # # Save to session_state history
            # if "prediction_history" not in st.session_state:
            #     st.session_state.prediction_history = []

            # st.session_state.prediction_history.append({
            #     "User": st.session_state.username,
            #     "Country": country,
            #     "Education": edlevel,
            #     "Experience": years_code,
            #     "Predicted Salary": f"${salary:,.2f}"
            # })
            # Save prediction to SQLite DB
            cursor.execute("""
                INSERT INTO history (username, country, education, experience, predicted_salary)
                VALUES (?, ?, ?, ?, ?)
            """, (st.session_state.username, country, edlevel, years_code, f"${salary:,.2f}"))
            conn.commit()


        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    st.markdown("#### ℹ️ Disclaimer")
    st.info("""
    This prediction is based on historical Stack Overflow developer survey data.
    Salaries can vary widely depending on role, region, and negotiation.
    """)

st.markdown("### 📁 Prediction History")
# Fetch history from DB
cursor.execute("SELECT country, education, experience, predicted_salary FROM history WHERE username=?", (st.session_state.username,))
records = cursor.fetchall()

if records:
    history_df = pd.DataFrame(records, columns=["Country", "Education", "Experience", "Predicted Salary"])
    st.table(history_df)

    csv = history_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download History as CSV",
        data=csv,
        file_name='salary_predictions.csv',
        mime='text/csv')
else:
    st.info("No predictions yet.")



st.markdown("## 📌 About this Project")
st.write("""
This app predicts the estimated salary of software developers based on their background, 
using data from the Stack Overflow Developer Survey.
""")

st.markdown("## 🧠 How the Model Works")
st.write("""
We trained a machine learning model on cleaned salary data. 
Inputs include country, education level, years of experience and roles.
""")

st.markdown("## 📂 Data Source")
st.write("""
Data is sourced from the Stack Overflow Developer Survey.
""")

st.markdown("----")
st.markdown("<h2 style='text-align: center; color: #2c3e50;'>📊 Salary Insights Dashboard</h2>", unsafe_allow_html=True)
st.markdown("### A visual summary of global software developer salaries based on education, roles, experience, and location.")
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
>>>>>>> 79ca29b79f8229423c01c0826a9bbcdf56880f84
