from model import model, le_country, le_edlevel
import numpy as np

def predict_salary(country, edlevel, years_code):
    # Encode categorical features using the label encoders
    country_enc = le_country.transform([country])[0]
    edlevel_enc = le_edlevel.transform([edlevel])[0]

    # Prepare input in the correct shape for prediction
    features = np.array([[country_enc, edlevel_enc, years_code]])
    
    # Make prediction using the loaded model
    predicted_salary = model.predict(features)[0]

    return predicted_salary
