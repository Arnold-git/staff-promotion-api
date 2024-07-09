from typing import Any

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.api_v1.api import api_router
from app.config import settings
import logging
import uvicorn
from app.pipeline import load_encoders, load_model
from contextlib import asynccontextmanager
from app.utils.fastapi_globals import g, GlobalsMiddleware


def customise_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="StaffPromotionAPI",
        version="1.0",
        description="Staff Promotion API to predict staff promotion",
        routes=app.routes,
        servers=None
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    logging.info("loading model")
    model = load_model(settings.MODEL_PATH)
    logging.info("model load successful")
    logging.info("loading encoder")
    encoders = load_encoders(settings.ENCODER_PATH)
    logging.info("encoder loaded successfully")
    g.set_default("model", model)
    g.set_default("encoders", encoders)
    yield
    # Clean up the ML models and release the resources
    del model
    del encoders
    g.cleanup()



app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


root_router = APIRouter()

@root_router.get("/")
def index(request: Request) -> Any:
    """
    Basic HTML response
    """
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to Staff Promotion API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)
app.add_middleware(GlobalsMiddleware)
customise_openapi(app)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)