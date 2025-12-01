from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from src.shared.config import settings


engine = create_engine(
    settings.get_database_url,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False
)
Base = declarative_base()


async def get_session() -> Session:
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
