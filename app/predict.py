from app.pipeline import apply_encoders, add_age_and_experience, load_model, load_encoders
import pandas as pd
from typing import Union
from app.config import __version__ as _version
from app.utils.fastapi_globals import g
import logging

def predict_staff_promotion(input_data: 
                    Union[pd.DataFrame, dict]) -> dict:
        
        input_df = pd.DataFrame(input_data, index=[0])

        relevant_data = input_df.drop(columns=['EmployeeNo'],axis =1)

        # get the loaded model and encoder
        model = g.model
        encoders = g.encoders
        relevant_data_encoded = apply_encoders(relevant_data, encoders)
        
        relevant_data_final = add_age_and_experience(relevant_data_encoded)
        
        # Make predictions
        prediction = model.predict(relevant_data_final)[0]
        predictions_prob = model.predict_proba(relevant_data_final)[:, 1]

        return {
            "prediction": int(prediction),
            "prediction_prob": float(predictions_prob[0]),
            "model_version": f"{_version}"
        }

