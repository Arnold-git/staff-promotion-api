from fastapi.security.api_key import APIKeyHeader
from fastapi import HTTPException, status
from fastapi import Security, status
from app.config import settings


api_key_header_auth = APIKeyHeader(
    name="X-API-KEY",
    description="Mandatory API Token, required for all endpoints",
    auto_error=True,
)

async def get_api_key(api_key_header: str = Security(api_key_header_auth)):

    if not check_api_key(api_key_header):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    

def check_api_key(api_key):
    if api_key == settings.api_key:
        return True