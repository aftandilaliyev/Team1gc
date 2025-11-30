from fastapi import FastAPI
from loguru import logger

from src.domains.health.router import router as health_router
from src.domains.auth.router import router as auth_router

def _setup_router(app: FastAPI):
    app.include_router(health_router)
    app.include_router(auth_router)
    # TODO: Include the routers from the domains
    ...

def get_app() -> FastAPI:
    app = FastAPI(
        title="Gem Store API",
        description="Gem Store API",
        version="0.1.0",
    )
    _setup_router(app)
    logger.info("Application initialized")
    return app
