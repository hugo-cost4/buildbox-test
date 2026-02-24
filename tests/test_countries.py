import pytest
from httpx import AsyncClient, ASGITransport, HTTPStatusError, RequestError, Response, Request
from unittest.mock import patch
from app.main import app

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_get_countries_success(async_client):
    """Testa se a rota retorna com sucesso a lista de países da API real (ou cacheada)"""
    response = await async_client.get("/countries")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "name" in data[0]
    assert "official_name" in data[0]
    assert "flag_url" in data[0]
    assert "is_long_name" in data[0]

@pytest.mark.asyncio
async def test_get_countries_with_search_filter(async_client):
    """Testa o filtro de busca básico"""
    response = await async_client.get("/countries?search=Brazil")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    
    # Verifica se encontrou Brasil
    brazil_found = any("brazil" in str(country["name"]).lower() for country in data)
    assert brazil_found

@pytest.mark.asyncio
async def test_get_countries_search_case_insensitive(async_client):
    """Testa se a busca ignora maiúsculas e minúsculas (case insensitive)"""
    # Buscando de forma bagunçada
    response = await async_client.get("/countries?search=bRaZiL")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) >= 1
    # Garante que o resultado que voltou contém "Brazil"
    assert "Brazil" in [c["name"] for c in data]

@pytest.mark.asyncio
async def test_get_countries_search_not_found(async_client):
    """Testa o cenário onde a busca não encontra nenhum país"""
    response = await async_client.get("/countries?search=PaísQueNaoExiste123")
    assert response.status_code == 200
    data = response.json()
    
    # Deve retornar uma lista vazia
    assert isinstance(data, list)
    assert len(data) == 0

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_external_api_http_error(mock_get, async_client):
    """
    Testa o tratamento de erro da nossa API caso a API do restcountries retorne um erro (ex: 500 deles).
    A nossa API DEVE retornar 502 Bad Gateway conforme a regra do teste.
    """
    # Simulando um erro de HTTP 500 do servidor original
    mock_request = Request("GET", "https://restcountries.com/v3.1/all?fields=name,flags")
    mock_response = Response(500, request=mock_request)
    mock_get.side_effect = HTTPStatusError("Internal Server Error", request=mock_request, response=mock_response)
    
    response = await async_client.get("/countries")
    
    assert response.status_code == 502
    assert response.json()["detail"] == "Erro de comunicação com a API externa (Downstream error)."

@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_external_api_connection_error(mock_get, async_client):
    """
    Testa o tratamento de erro caso a API do restcountries fique offline / timeout.
    Também deve retornar 502 Bad Gateway.
    """
    # Simulando timeout/queda de rede
    mock_request = Request("GET", "https://restcountries.com/v3.1/all?fields=name,flags")
    mock_get.side_effect = RequestError("Timeout duration reached", request=mock_request)
    
    response = await async_client.get("/countries")
    
    assert response.status_code == 502
    assert response.json()["detail"] == "Erro de conexão com a API externa."
