<<<<<<< HEAD
import joblib

# Load the trained model from the correct file and folder
model = joblib.load("model.pkl")

# Load all the correct label encoders from the notebooks folder
le_country = joblib.load("le_country.pkl")
le_edlevel = joblib.load("le_edlevel.pkl")
le_role = joblib.load("le_role.pkl")
=======
import joblib

# Load the trained model
model = joblib.load('salary_predictor_model.pkl')

# Load label encoders (if you saved them separately)
le_country = joblib.load('le_country.pkl')
le_edlevel = joblib.load('le_edlevel.pkl')
>>>>>>> 79ca29b79f8229423c01c0826a9bbcdf56880f84
