# app/infrastructure/external_api.py
from app.infrastructure.http_client import HTTPClient
from app.config import settings

class RestCountriesAPI:
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    async def get_all_countries(self) -> list[dict]:
        return await self.http_client.fetch(settings.REST_COUNTRIES_URL)
