from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import jwt
from fastapi import HTTPException, status
from sqlalchemy.sql import roles

from src.shared.models.user import User, get_password_hash, verify_password
from src.shared.schemas.user import AuthResponse, UserCreate, UserLogin, UserResponse, UserRoleEnum
from src.shared.config import settings


class AuthService:
    def __init__(self, session) -> None:
        self.session = session

    def _create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def _verify_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None

    def _get_user_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(User.username == username).first()

    def _get_user_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_access_token(self, token: str) -> Optional[User]:
        payload = self._verify_token(token)
        if not payload:
            return None
        username = payload.get("sub")
        if not username:
            return None
        return self._get_user_by_username(username)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self._get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def register_user(self, user_data: UserCreate) -> UserResponse:
        # Check if user already exists
        if self._get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if self._get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            role=user_data.role,
            is_active=True
        )
        
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        
        # Return user response schema
        return UserResponse(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            role=db_user.role
        )

    def login_user(self, login_data: UserLogin) -> AuthResponse:
        user = self.authenticate_user(login_data.username, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return AuthResponse(
            access_token=access_token,
            user=UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                is_active=user.is_active,
                created_at=user.created_at,
                role=user.role
            )
        )
