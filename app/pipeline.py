import datetime
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
import joblib
import logging
import os
import joblib

from app.config import __version__ as _version

PACKAGE_ROOT = "api"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def custom_label_encoder(X, columns):
    encoders = {}
    X_encoded = X.copy()
    logging.info("Encoding begins...")
    for column in columns:
        encoder = LabelEncoder()
        X_encoded[column + '_encoded'] = encoder.fit_transform(X[column])
        encoders[column] = encoder
    logging.info("Encoding completed...")
    X_encoded.drop(columns=columns, inplace=True)
    logging.info("Persisting encoding")
    joblib.dump(encoders, 'encoder.joblib')
    logging.info("Persisting encoding completed...")
    return X_encoded, encoders

def calculate_years(year):
    year = datetime.datetime.strptime(str(year), "%Y")
    years = datetime.datetime.strptime("2019", "%Y") - year
    return years.days // 365

def add_age_and_experience(X):
    X = X.copy()
    X['age'] = X['Year_of_birth'].apply(calculate_years)
    X['no_of_years_in_the_company'] = X['Year_of_recruitment'].apply(calculate_years)
    X.drop(columns=['Year_of_birth', 'Year_of_recruitment'], inplace=True)
    return X

def preprocess_data(X, cat_columns):
    X_encoded, encoders = custom_label_encoder(X, cat_columns)
    X_final = add_age_and_experience(X_encoded)
    return X_final, encoders


def load_model(model_path: str):
    return joblib.load(model_path)

def load_encoders(encoders_path: str):
    return joblib.load(encoders_path)

def apply_encoders(X, encoders):
    X_encoded = X.copy()
    for column, encoder in encoders.items():
        X_encoded[column + '_encoded'] = X[column].apply(
            lambda x: encoder.transform([x])[0] if x in encoder.classes_ else -1
        )
    X_encoded.drop(columns=encoders.keys(), inplace=True)
    return X_encoded


def save_model(model, folder_path, model_name=f"model_{_version}.joblib"):
    model_path = os.path.join(folder_path, model_name)

    # Check if the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Check if the folder is empty
    if os.listdir(folder_path):
        # If not empty, delete the existing model
        if os.path.exists(model_path):
            os.remove(model_path)
            logging.info(f"Deleted existing model: {model_path}")

    # Save the new model
    joblib.dump(model, model_path)
    logging.info(f"Saved new model: {model_path}")


# if __name__ == "__main__":
#     # data = "data/train.csv"
#     # run_training(data)
#     print(_version)
