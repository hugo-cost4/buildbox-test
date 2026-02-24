# Google Colab Version
import nest_asyncio
import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, HttpUrl, Field, computed_field
import httpx
from typing import Optional
import threading

nest_asyncio.apply()

app = FastAPI(title="Buildbox Test - Colab Version")

class Country(BaseModel):
    name: str = Field(..., description="Nome comum do país")
    official_name: str = Field(..., description="Nome oficial do país")
    flag_url: HttpUrl = Field(..., description="URL da bandeira (formato svg)")

    @computed_field
    def is_long_name(self) -> bool:
        return len(self.name) > 15

async def fetch_countries():
    url = "https://restcountries.com/v3.1/all?fields=name,flags"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Erro de comunicação com a API externa (Downstream error).")

async def get_countries_service(search: Optional[str] = None):
    raw_data = await fetch_countries()
    countries = []
    
    for item in raw_data:
        common_name = item.get("name", {}).get("common", "")
        official_name = item.get("name", {}).get("official", "")
        flag_url = item.get("flags", {}).get("svg") or item.get("flags", {}).get("png", "")
        
        if not flag_url:
            continue
            
        if search and search.lower() not in common_name.lower():
            continue
            
        countries.append(Country(name=common_name, official_name=official_name, flag_url=flag_url))
        
    return countries

@app.get("/countries", response_model=list[Country])
async def list_countries(search: Optional[str] = Query(None)):
    return await get_countries_service(search)

def run_server():
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8000))
    sock.close()
    
    if result == 0:
        print("Server is already running in background: http://127.0.0.1:8000")
        return
        
    print("Starting server in background: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

thread = threading.Thread(target=run_server)
thread.daemon = True
thread.start()

async def test_api():
    await asyncio.sleep(1)
    
    async with httpx.AsyncClient() as client:
        print("\n--- Testing GET /countries ---")
        response = await client.get("http://127.0.0.1:8000/countries")
        print("Status:", response.status_code)
        
        if response.status_code == 200:
            data = response.json()
            print("Total returned:", len(data))
            print("Example:")
            print(data[:2])
        else:
            print("Error:", response.text)
            
        print("\n--- Testing GET /countries?search=brazil ---")
        search_response = await client.get("http://127.0.0.1:8000/countries?search=brazil")
        print("Status:", search_response.status_code)
        
        if search_response.status_code == 200:
            data = search_response.json()
            print(f"Total returned: {len(data)}")
            if len(data) > 0:
                import json
                print("Example:")
                print(json.dumps(data[:2], indent=2))
            else:
                print("No countries found with this term.")
        else:
            print("Error searching:", search_response.text)
                
await test_api()
