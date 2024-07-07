from app.pipeline import apply_encoders, add_age_and_experience, load_model, load_encoders
import pandas as pd
from typing import Union
from app.config import __version__ as _version
from app.utils.fastapi_globals import g
import logging

def predict_staff_promotion(input_data: 
                    Union[pd.DataFrame, dict]) ->dict:

    test_df = pd.DataFrame(input_data, index=[0])

    X_test = test_df.drop(columns=['EmployeeNo'],axis =1)

    model = g.model
    encoders = g.encoders
    logging.info(f"Encoder {encoders}")
    X_test_encoded = apply_encoders(X_test, encoders)
    
    X_test_final = add_age_and_experience(X_test_encoded)
    
    # Make predictions
    prediction = model.predict(X_test_final)[0]
    predictions_prob = model.predict_proba(X_test_final)[:, 1]

    return {
        "prediction": int(prediction),
        "prediction_prob": float(predictions_prob[0]),
        "model_version": f"{_version}"
    }


# if __name__ == "__main__":
#     data = {'EmployeeNo': 'YAK/S/00011',
#             'Division': 'Information Technology and Solution Support',
#             'Qualification': "nan",
#             'Gender': 'Male',
#             'Channel_of_Recruitment': 'Direct Internal process',
#             'Trainings_Attended': 2,
#             'Year_of_birth': 1991,
#             'Last_performance_score': 0.0,
#             'Year_of_recruitment': 2018,
#             'Targets_met': 0,
#             'Previous_Award': 0,
#             'Training_score_average': 69,
#             'State_Of_Origin': 'OGUN',
#             'Foreign_schooled': 'Yes',
#             'Marital_Status': 'Married',
#             'Past_Disciplinary_Action': 'No',
#             'Previous_IntraDepartmental_Movement': 'No',
#             'No_of_previous_employers': '1'}
#     print(predict_on_test(data))
