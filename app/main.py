# app/main.py
from fastapi import FastAPI
from app.presentation.routes import router as country_router
from prometheus_fastapi_instrumentator import Instrumentator

def create_app() -> FastAPI:
    app = FastAPI(
        title="Buildbox Test API",
        description="API de Consulta de Países com Clean Architecture",
        version="1.0.0",
    )
    
    app.include_router(country_router)
    Instrumentator().instrument(app).expose(app)
    
    return app

app = create_app()
