import joblib

# Load the trained model from the correct file and folder
model = joblib.load("model.pkl")

# Load all the correct label encoders from the notebooks folder
le_country = joblib.load("le_country.pkl")
le_edlevel = joblib.load("le_edlevel.pkl")
le_role = joblib.load("le_role.pkl")