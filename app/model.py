import joblib

# Load the trained model
model = joblib.load('salary_predictor_model.pkl')

# Load label encoders (if you saved them separately)
le_country = joblib.load('le_country.pkl')
le_edlevel = joblib.load('le_edlevel.pkl')
