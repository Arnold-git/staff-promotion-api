from fastapi import APIRouter, Response
from app.schema.error import ServiceError
from app.schema.response import StaffPromotionResponse, StaffPromotionResult
from app.schema.staff_info import StaffInfo
router = APIRouter()
import logging
from app.predict import predict_staff_promotion
from pydantic import ValidationError

@router.post("/predict-staff-promotion", response_model=StaffPromotionResponse, description = "Staff Promotion API")
def sentiment_analysis(
    httpResponse: Response,
    inputData: StaffInfo
):
  
  try:
    # use Pydantic. model_dump() method that returns a dict with the model's data
    staff_details = inputData.model_dump()
  
    result = predict_staff_promotion(staff_details)
    
    staff_promotion_result = StaffPromotionResult(
      promote="Yes" if result.get("prediction") == 1 else "No",
      prediction_proba = result.get("prediction_prob"),
      staff_info=staff_details,
      version=result.get("model_version")
    )
    response = StaffPromotionResponse(
      success=True,
      data=staff_promotion_result,
  
    )
    logging.info(f"prediction result {response}")
    return response
  except ServiceError as e:
    httpResponse.status_code = 400
    logging.warning(f"Prediction error: {e}")
    response = StaffPromotionResponse(
      success=False,
      message=e.message
    )

    return response