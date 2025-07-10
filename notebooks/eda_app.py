# Import required libraries
import streamlit as st                    # For building the web interface
import pandas as pd                      # For data manipulation
import matplotlib.pyplot as plt          # For plotting graphs
import seaborn as sns                    # For advanced visualizations

# Set Streamlit page title
st.title("📊 Salary Data - Exploratory Data Analysis")

# Load dataset (make sure the path is correct relative to ths file)
df = pd.read_csv("C:/Users/LENOVO/Downloads/Salary Predictor/data/survey_results_public.csv")

# Show a preview of the dataset
st.subheader("🔍 Dataset Preview")
st.dataframe(df.head())  # Display first 5 rows of the dataframe

# Basic dataset information
st.subheader("📈 Dataset Info")
st.write("Number of Rows:", df.shape[0])  # Total number of rows
st.write("Number of Columns:", df.shape[1])  # Total number of columns

# Show summary statistics for numeric columns
st.subheader("📊 Summary Statistics")
st.write(df.describe())  # Descriptive statistics like mean, std, etc.

# Show missing values (if any)
st.subheader("❓ Missing Values")
missing = df.isnull().sum()
missing = missing[missing > 0]  # Only show columns with missing values
st.write(missing)

# Salary distribution
st.subheader("💰 Salary Distribution")
if 'ConvertedCompYearly' in df.columns:
    fig, ax = plt.subplots()
    sns.histplot(df['ConvertedCompYearly'].dropna(), kde=True, bins=30, ax=ax)
    ax.set_xlabel("Converted Compensation (Yearly, USD)")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Yearly Salary (in USD)")
    st.pyplot(fig)

    # === Your new added visualization sections ===

    # Salary by country boxplot
    st.subheader("🌍 Salary by Country (Boxplot)")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x='Country', y='ConvertedCompYearly', ax=ax2)
    plt.xticks(rotation=45)
    ax2.set_ylabel("Yearly Salary (USD)")
    st.pyplot(fig2)

    # Salary by education level boxplot
    st.subheader("🎓 Salary by Education Level")
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df, x='EdLevel', y='ConvertedCompYearly', ax=ax3)
    plt.xticks(rotation=45)
    ax3.set_ylabel("Yearly Salary (USD)")
    st.pyplot(fig3)

    # Country-wise filtering and histogram
    st.subheader("🔎 Country-wise Filtering")
    selected_country = st.selectbox("Select a country to explore:", df['Country'].unique())
    filtered_data = df[df['Country'] == selected_country]

    st.write(f"Salary distribution in {selected_country}")
    fig4, ax4 = plt.subplots()
    sns.histplot(filtered_data['ConvertedCompYearly'].dropna(), kde=True, bins=20, ax=ax4)
    ax4.set_xlabel("Yearly Salary (USD)")
    st.pyplot(fig4)

else:
    st.warning("'ConvertedCompYearly' column not found in dataset.")