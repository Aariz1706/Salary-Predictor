<<<<<<< HEAD
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

# Load data
df = pd.read_csv("../data/survey_results_public.csv")

# Drop rows with missing salary or key features
df = df.dropna(subset=["Country", "EdLevel", "YearsCodePro", "ConvertedCompYearly", "DevType"])

# Clean "YearsCodePro" column
def clean_experience(x):
    if "Less than" in str(x):
        return 0.5
    elif "More than" in str(x):
        return 51
    try:
        return float(x)
    except:
        return None

df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
df = df.dropna(subset=["YearsCodePro"])

# Rename "DevType" to "Role" (match your app UI)
df["Role"] = df["DevType"]

# Keep only roles that match your dropdown (optionally consolidate others into "Other")
allowed_roles = [
    "Developer, back-end", "Developer, front-end", "Developer, full-stack",
    "Developer, mobile", "Data scientist or machine learning specialist",
    "Engineer, data", "DevOps specialist", "System administrator", "Designer"
]
df["Role"] = df["Role"].apply(lambda x: x if x in allowed_roles else "Other")

# Clean Education
def simplify_ed(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree (B.A., B.S., B.Eng., etc.)"
    elif "Master’s degree" in x:
        return "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)"
    elif "Doctoral" in x:
        return "Other doctoral degree (Ph.D., Ed.D., etc.)"
    elif "Associate" in x:
        return "Associate degree (A.A., A.S., etc.)"
    elif "Professional" in x:
        return "Professional degree (JD, MD, etc.)"
    elif "Some college" in x:
        return "Some college/university study without earning a degree"
    elif "Secondary school" in x:
        return "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)"
    elif "Primary" in x:
        return "Primary/elementary school"
    else:
        return "Something else"

df["EdLevel"] = df["EdLevel"].apply(simplify_ed)

# Select relevant columns
df = df[["Country", "EdLevel", "YearsCodePro", "Role", "ConvertedCompYearly"]]
df = df.rename(columns={
    "ConvertedCompYearly": "Salary",
    "YearsCodePro": "Experience"
})

# Encode categorical data
le_country = LabelEncoder()
le_edlevel = LabelEncoder()
le_role = LabelEncoder()

df["Country"] = le_country.fit_transform(df["Country"])
df["EdLevel"] = le_edlevel.fit_transform(df["EdLevel"])
df["Role"] = le_role.fit_transform(df["Role"])

# Split data and train model
X = df[["Country", "EdLevel", "Experience", "Role"]]
y = df["Salary"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, "model.pkl")
joblib.dump(le_country, "le_country.pkl")
joblib.dump(le_edlevel, "le_edlevel.pkl")
joblib.dump(le_role, "le_role.pkl")

print("✅ Model and encoders saved successfully!")
=======
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib

# Load data
df = pd.read_csv("../data/survey_results_public.csv")

# Drop rows with missing salary or key features
df = df.dropna(subset=["Country", "EdLevel", "YearsCodePro", "ConvertedCompYearly", "DevType"])

# Clean "YearsCodePro" column
def clean_experience(x):
    if "Less than" in str(x):
        return 0.5
    elif "More than" in str(x):
        return 51
    try:
        return float(x)
    except:
        return None

df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
df = df.dropna(subset=["YearsCodePro"])

# Rename "DevType" to "Role" (match your app UI)
df["Role"] = df["DevType"]

# Keep only roles that match your dropdown (optionally consolidate others into "Other")
allowed_roles = [
    "Developer, back-end", "Developer, front-end", "Developer, full-stack",
    "Developer, mobile", "Data scientist or machine learning specialist",
    "Engineer, data", "DevOps specialist", "System administrator", "Designer"
]
df["Role"] = df["Role"].apply(lambda x: x if x in allowed_roles else "Other")

# Clean Education
def simplify_ed(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree (B.A., B.S., B.Eng., etc.)"
    elif "Master’s degree" in x:
        return "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)"
    elif "Doctoral" in x:
        return "Other doctoral degree (Ph.D., Ed.D., etc.)"
    elif "Associate" in x:
        return "Associate degree (A.A., A.S., etc.)"
    elif "Professional" in x:
        return "Professional degree (JD, MD, etc.)"
    elif "Some college" in x:
        return "Some college/university study without earning a degree"
    elif "Secondary school" in x:
        return "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)"
    elif "Primary" in x:
        return "Primary/elementary school"
    else:
        return "Something else"

df["EdLevel"] = df["EdLevel"].apply(simplify_ed)

# Select relevant columns
df = df[["Country", "EdLevel", "YearsCodePro", "Role", "ConvertedCompYearly"]]
df = df.rename(columns={
    "ConvertedCompYearly": "Salary",
    "YearsCodePro": "Experience"
})

# Encode categorical data
le_country = LabelEncoder()
le_edlevel = LabelEncoder()
le_role = LabelEncoder()

df["Country"] = le_country.fit_transform(df["Country"])
df["EdLevel"] = le_edlevel.fit_transform(df["EdLevel"])
df["Role"] = le_role.fit_transform(df["Role"])

# Split data and train model
X = df[["Country", "EdLevel", "Experience", "Role"]]
y = df["Salary"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and encoders
joblib.dump(model, "model.pkl")
joblib.dump(le_country, "le_country.pkl")
joblib.dump(le_edlevel, "le_edlevel.pkl")
joblib.dump(le_role, "le_role.pkl")

print("✅ Model and encoders saved successfully!")
>>>>>>> 79ca29b79f8229423c01c0826a9bbcdf56880f84
