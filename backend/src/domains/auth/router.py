from typing import Annotated, Dict, Any

from fastapi import APIRouter, Header, status, Depends

from src.shared.schemas.user import AuthResponse, UserCreate, UserLogin, UserResponse
from src.domains.auth.service import AuthService
from src.shared.dependencies.auth import get_auth_service


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, service: Annotated[AuthService, Depends(get_auth_service)]) -> UserResponse:
    """
    Register a new user with email, username, and password.
    """
    return service.register_user(user_data)

@router.post("/login", response_model=AuthResponse)
def login(login_data: UserLogin, service: Annotated[AuthService, Depends(get_auth_service)]) -> Dict[str, Any]:
    """
    Login with username and password to get access token.
    """
    return service.login_user(login_data)

@router.get("/me", response_model=UserResponse)
def get_me(
        access_token: Annotated[str, Header(alias="X-Auth-Header")],
        service: Annotated[AuthService, Depends(get_auth_service)]
    ) -> UserResponse:
    """
    Get current user information from JWT token.
    """
    return service.get_current_user(access_token)
