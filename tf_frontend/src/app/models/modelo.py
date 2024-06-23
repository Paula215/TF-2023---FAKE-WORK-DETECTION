import pandas as pd
from joblib import load

from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# One-Hot Encoding de variables categóricas
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

# Selección de variables categóricas y numéricas
categorical_features = ['title', 'location', 'company_profile', 'description', 'employment_type', 'required_experience', 'function']

from joblib import load

categorical_features = ['title', 'location', 'company_profile', 'description', 'employment_type', 'required_experience', 'function']

def predict_new_entry(title, location, company_profile, description, employment_type, required_experience, function):
    # Cargar el modelo y el codificador preentrenados
    clf = load('./models/clf.joblib')
    encoder = load('./models/encoder.joblib')
    
    new_data = {
        'title': [title],
        'location': [location],
        'company_profile': [company_profile],
        'description': [description],
        'employment_type': [employment_type],
        'required_experience': [required_experience],
        'function': [function]
    }
    new_df = pd.DataFrame(new_data)

    # One-Hot Encoding
    encoded_new_features = encoder.transform(new_df[categorical_features])
    encoded_new_df = pd.DataFrame(encoded_new_features, columns=encoder.get_feature_names_out(categorical_features))

    # Predecir con el modelo entrenado
    prediction = clf.predict(encoded_new_df)
    return prediction[0]