from fastapi import APIRouter
from app.api.api_v1.endpoints import health
from app.api.api_v1.endpoints import staff_promotion
api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(staff_promotion.router, tags=["Sentiment Analysis"])