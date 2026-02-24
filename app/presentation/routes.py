# app/presentation/routes.py
from fastapi import APIRouter, Query, Depends
from typing import Optional

from app.domain.models import Country
from app.application.services import CountryService
from app.infrastructure.http_client import HTTPClient
from app.infrastructure.external_api import RestCountriesAPI

router = APIRouter()

def get_country_service() -> CountryService:
    http_client = HTTPClient()
    external_api = RestCountriesAPI(http_client)
    return CountryService(external_api)

@router.get("/countries", response_model=list[Country])
async def list_countries(
    search: Optional[str] = Query(None, description="Filtro de busca (case insensitive) pelo nome comum do país."),
    service: CountryService = Depends(get_country_service)
):
    return await service.get_countries(search=search)
