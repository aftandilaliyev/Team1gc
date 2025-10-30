from fastapi import FastAPI

from src.domains.health.router import router as health_router

def _setup_router(app: FastAPI):
    app.include_router(health_router)
    # TODO: Include the routers from the domains
    ...

def get_app() -> FastAPI:
    app = FastAPI(
        title="Gem Store API",
        description="Gem Store API",
        version="0.1.0",
    )
    _setup_router(app)
    return app
