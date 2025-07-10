from model import model, le_country, le_edlevel, le_role
import numpy as np

def predict_salary(country, edlevel, years_code, role):
    # Encode all categorical features using the label encoders
    country_enc = le_country.transform([country])[0]
    edlevel_enc = le_edlevel.transform([edlevel])[0]
    role_enc = le_role.transform([role])[0]

    # Prepare input for prediction
    features = np.array([[country_enc, edlevel_enc, years_code, role_enc]])
    
    # Make prediction using the model
    predicted_salary = model.predict(features)[0]
    return predicted_salary
