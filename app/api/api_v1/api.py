from fastapi import APIRouter, Depends
from app.api.api_v1.endpoints import health
from app.api.api_v1.endpoints import staff_promotion
from app.utils.api_key_middleware import get_api_key
api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(staff_promotion.router, tags=["Predict Staff Promotion"], dependencies=[Depends(get_api_key)])