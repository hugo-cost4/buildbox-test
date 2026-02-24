# Buildbox Backend Challenge

Esta é a implementação do teste técnico para a vaga de desenvolvedor Backend Pleno/Sênior na Buildbox, utilizando **FastAPI**, **Pydantic v2** e **Clean Architecture**.

## 🚀 Tecnologias Utilizadas

- **FastAPI**: Criação rápida e assíncrona de rotas HTTP.
- **Pydantic v2**: Validação de dados e modelagem de negócio (`@computed_field`).
- **httpx**: Cliente HTTP assíncrono para consumir APIs externas.
- **pytest & pytest-asyncio**: Testes automatizados cobrindo a lógica e a API.
- **Prometheus Instrumentator**: Exposição da rota `/metrics` provendo observabilidade.
- **Docker & Docker Compose**: Empacotamento para fácil execução.

## 🏗️ Arquitetura

O projeto foi construído seguindo os princípios de **Clean Architecture** (um dos diferenciais da vaga), possuindo a separação clássica:

- `domain/`: Contém os modelos base (Pydantic models) e lógicas inerentes às entidades (`is_long_name`).
- `application/`: Responsável pelo Service principal, que orquestra a busca de dados e aplicação de filtros (case-insensitive search).
- `infrastructure/`: Implementação do cliente HTTP assíncrono (`http_client.py`) e conexão com a API Extena. Cuida dos tratamentos de erros de rede HTTP (502 Gateway Error).
- `presentation/`: Exposição das rotas FastApi.

---

## 💻 Execução com Docker (Recomendado)

A forma mais rápida de visualizar o projeto com todas as suas dependências isoladas:

```bash
docker-compose up --build
```

A API estará disponível no `http://localhost:8000/countries`

Para acessar as métricas do **Prometheus**:
`http://localhost:8000/metrics`

---

## 🧪 Execução de Testes

Os testes garantem a eficácia da aplicação, simulando requisições assíncronas no contexto do FastAPI.
(Você precisará ter o python 3.11+ instalado)

```bash
# 1. Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Rode os testes
pytest tests/
```

---

## 📝 Versão Executável: Google Colab

Conforme a exigência estrita do desafio ("_O teste deverá ser implementado e executado no Google Colab_"), disponibilizei uma versão condensada de toda a lógica do repositório em um único script:

[📝 Arquivo colab_version.py](./colab_version.py)

Basta copiar o conteúdo do arquivo `colab_version.py` e colá-lo em uma célula do **Google Colab**. O script utiliza `nest_asyncio` e levanta o servidor `uvicorn` localmente no Colab em uma thread segregada, rodando as validações automáticas na sequência.

---

## 📌 Requisitos Atendidos

✅ Utilização exclusiva de FastAPI e Pydantic v2
✅ Requisição HTTP assíncrona usando `httpx.AsyncClient`
✅ Modelagem de Response através de `response_model`
✅ Tratamento robusto para exceções da API base (HTTP 502 em caso de erro)
✅ Sem utilização da lib síncrona `requests`
✅ Regra `is_long_name` criada internamente via Pydantic model (`computed_field`)
✅ Busca `case-insensitive` e separada da camada de Infra e Apresentação
✅ Google Colab version
✅ Qualidade e Boas práticas (Clean Arch)
✅ Observabilidade (Prometheus metrics)
