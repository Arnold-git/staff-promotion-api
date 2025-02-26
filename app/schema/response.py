
from typing import Optional
from pydantic import BaseModel

class BaseResponse(BaseModel):
    success: bool
    message: Optional[str] = None


class StaffPromotionResult(BaseModel):
    promote: Optional[str]
    prediction_proba: Optional[float]
    version: Optional[str]
    staff_info: Optional[dict]

class StaffPromotionResponse(BaseResponse):
    data: Optional[StaffPromotionResult]
