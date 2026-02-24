# Teste Técnico — FastAPI + Pydantic v2

## Objetivo

Desenvolver uma API utilizando FastAPI contendo apenas uma rota, que será responsável por consultar uma API pública externa, tratar os dados e retornar uma resposta estruturada.

## Requisitos

Você deverá criar uma rota HTTP GET com o seguinte path: 
```
GET /countries
```

Essa rota deverá:

1. Realizar uma chamada assíncrona para a API externa: https://restcountries.com/v3.1/all?fields=name,flags
2. Processar os dados recebidos.
3. Retornar uma lista estruturada com os campos especificados abaixo comforme campo Estruta da Resposta.
4. Query Parameter (Opcional) A rota deve aceitar um parâmetro opcional: 
```
?search=texto
```

## Regras:

O filtro deve ser aplicado sobre o campo name (nome comum do país). A busca deve ser case insensitive. Caso o parâmetro não seja informado, todos os países devem ser retornados.

## Estrutura da Resposta:
```
[
  {
    "name": "Brazil",
    "official_name": "Federative Republic of Brazil",
    "flag_url": "https://flagcdn.com/br.svg",
    "is_long_name": false
  }
]
```
## Campos obrigatórios:

name → Nome comum do país 
official_name → Nome oficial do país 
flag_url → URL da bandeira (formato svg) 
is_long_name → Boolean

## Regra de Negócio: Utilizar FastAPI

1. Utilizar Pydantic v2
2. Utilizar requisição assíncrona com httpx.AsyncClient
3. Definir response_model
4. Implementar tratamento de erro:
5. Caso a API externa falhe, retornar status HTTP 502

## Restrições: Não é permitido:
1. Utilizar requests
2. Retornar os dados crus da API externa
3. Implementar a regra is_long_name diretamente na rota

## Execução Obrigatória O teste deverá ser implementado e executado no Google Colab.

Para validação, será utilizado o seguinte trecho de código para testar a rota:

```
print("Status:", response.status_code)
print("Total retornado:", len(response.json()))
print("Exemplo:")
print(response.json()[:2])
```

## Critérios de Avaliação:
1. Uso correto de async/await
2. Modelagem adequada com Pydantic v2
3. Clareza e organização do código
4. Separação adequada de responsabilidades
5. Tratamento correto de erros
6. Boa utilização de tipagem