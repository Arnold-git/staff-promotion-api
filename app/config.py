from pydantic import AnyHttpUrl, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  SecretStr
from typing import List, Union
from dotenv import load_dotenv
import os
import logging

load_dotenv


with open("app/VERSION") as version_file:
    __version__ = version_file.read().strip()

class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: None = logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Settings(BaseSettings):

    PROJECT_NAME: str = "Staff Promotion API"
    API_V1_STR: str = "/api/v1"
    # API_KEY: str = Field(alias=os.getenv("API_KEY"))
    SERVER_NAME: str = "StaffPromotionApp"
    MODEL_PATH: str = "app/trained_model/model_0.0.1.joblib"
    ENCODER_PATH: str = "app/trained_model/encoding.joblib"
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    model_config = SettingsConfigDict(env_file='app\.env', 
                                    env_file_encoding='utf-8')
    
    api_key: str


    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

settings = Settings()
logging = LoggingSettings()