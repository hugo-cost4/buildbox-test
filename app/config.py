# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REST_COUNTRIES_URL: str = "https://restcountries.com/v3.1/all?fields=name,flags"

settings = Settings()
