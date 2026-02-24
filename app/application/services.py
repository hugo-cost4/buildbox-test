# app/application/services.py
from typing import Optional
from app.infrastructure.external_api import RestCountriesAPI
from app.domain.models import Country

class CountryService:
    def __init__(self, external_api: RestCountriesAPI):
        self.external_api = external_api

    async def get_countries(self, search: Optional[str] = None) -> list[Country]:
        raw_data = await self.external_api.get_all_countries()
        
        countries = []
        for item in raw_data:
            name_data = item.get("name", {})
            flags_data = item.get("flags", {})
            
            common_name = name_data.get("common", "Unknown")
            official_name = name_data.get("official", "Unknown")
            
            flag_url = flags_data.get("svg") or flags_data.get("png", "")
            
            if not flag_url:
                continue
            
            country_obj = Country(
                name=common_name,
                official_name=official_name,
                flag_url=flag_url
            )
            
            if search:
                if search.lower() not in common_name.lower():
                    continue
                    
            countries.append(country_obj)
            
        return countries
