from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.auth.service import AuthService
from src.shared.database.connection import get_session


def get_auth_service(
    session: AsyncSession = Depends(get_session)
) -> AuthService:
    return AuthService(session)
