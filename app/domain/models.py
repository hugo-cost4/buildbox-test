# app/domain/models.py
from pydantic import BaseModel, HttpUrl, Field, computed_field

class CountryAPIResponse(BaseModel):
    name: dict
    flags: dict

class Country(BaseModel):
    name: str = Field(..., description="Nome comum do país")
    official_name: str = Field(..., description="Nome oficial do país")
    flag_url: HttpUrl = Field(..., description="URL da bandeira (formato svg)")

    @computed_field
    def is_long_name(self) -> bool:
        return len(self.name) > 25
