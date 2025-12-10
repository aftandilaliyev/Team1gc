from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.domains.health.router import router as health_router
from src.domains.auth.router import router as auth_router
from src.domains.products.router import router as products_router
from src.domains.buyers.router import router as buyers_router
from src.domains.sellers.router import router as sellers_router
from src.domains.suppliers.router import router as suppliers_router
from src.domains.webhooks.router import router as webhooks_router
from src.domains.uploads.router import router as uploads_router
from src.infrastructure.database.connection import init_database

def _setup_router(app: FastAPI):
    # Public routes
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(products_router, prefix="/api/v1")
    
    # Role-based routes
    app.include_router(buyers_router, prefix="/api/v1")
    app.include_router(sellers_router, prefix="/api/v1")
    app.include_router(suppliers_router, prefix="/api/v1")
    
    # Upload routes
    app.include_router(uploads_router, prefix="/api/v1")
    
    # Webhook routes
    app.include_router(webhooks_router, prefix="/api/v1")

def get_app() -> FastAPI:
    app = FastAPI(
        title="Gem Store API",
        description="Gem Store API",
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "https://team1gc.vercel.app", "https://www.fertit.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize database tables
    try:
        init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    _setup_router(app)
    logger.info("Application initialized")
    return app
