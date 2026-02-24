# app/infrastructure/http_client.py
import httpx
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class HTTPClient:
    async def fetch(self, url: str) -> list[dict]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Erro HTTP ao acessar {url}: {e.response.status_code}")
                raise HTTPException(status_code=502, detail="Erro de comunicação com a API externa (Downstream error).")
            except httpx.RequestError as e:
                logger.error(f"Erro de conexão ao acessar {url}: {e}")
                raise HTTPException(status_code=502, detail="Erro de conexão com a API externa.")
