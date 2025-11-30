import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import jwt

from src.domains.auth.service import AuthService
from src.shared.models.user import User
from src.shared.schemas.user import UserCreate, UserLogin, UserResponse, AuthResponse, UserRoleEnum


class TestAuthService:
    """Test suite for AuthService class."""

    def test_init(self, mock_session):
        """Test AuthService initialization."""
        service = AuthService(mock_session)
        assert service.session == mock_session

    @patch('src.domains.auth.service.jwt.encode')
    @patch('src.domains.auth.service.settings')
    def test_create_access_token_with_expires_delta(self, mock_settings, mock_jwt_encode, auth_service):
        """Test _create_access_token with custom expires_delta."""
        mock_settings.SECRET_KEY = "test_secret"
        mock_settings.ALGORITHM = "HS256"
        mock_jwt_encode.return_value = "test_token"
        
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=60)
        
        token = auth_service._create_access_token(data, expires_delta)
        
        assert token == "test_token"
        mock_jwt_encode.assert_called_once()
        call_args = mock_jwt_encode.call_args[0]
        assert call_args[0]["sub"] == "testuser"
        assert "exp" in call_args[0]

    @patch('src.domains.auth.service.jwt.encode')
    @patch('src.domains.auth.service.settings')
    def test_create_access_token_default_expiry(self, mock_settings, mock_jwt_encode, auth_service):
        """Test _create_access_token with default expiry."""
        mock_settings.SECRET_KEY = "test_secret"
        mock_settings.ALGORITHM = "HS256"
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        mock_jwt_encode.return_value = "test_token"
        
        data = {"sub": "testuser"}
        
        token = auth_service._create_access_token(data)
        
        assert token == "test_token"
        mock_jwt_encode.assert_called_once()

    @patch('src.domains.auth.service.jwt.decode')
    @patch('src.domains.auth.service.settings')
    def test_verify_token_success(self, mock_settings, mock_jwt_decode, auth_service):
        """Test _verify_token with valid token."""
        mock_settings.SECRET_KEY = "test_secret"
        mock_settings.ALGORITHM = "HS256"
        mock_jwt_decode.return_value = {"sub": "testuser", "exp": 1234567890}
        
        # Patch the settings import directly in the service module
        with patch('src.domains.auth.service.settings', mock_settings):
            result = auth_service._verify_token("valid_token")
        
        assert result == {"sub": "testuser", "exp": 1234567890}
        mock_jwt_decode.assert_called_once_with("valid_token", "test_secret", algorithms=["HS256"])

    @patch('src.domains.auth.service.jwt.decode')
    @patch('src.domains.auth.service.settings')
    def test_verify_token_invalid(self, mock_settings, mock_jwt_decode, auth_service):
        """Test _verify_token with invalid token."""
        mock_settings.SECRET_KEY = "test_secret"
        mock_settings.ALGORITHM = "HS256"
        mock_jwt_decode.side_effect = jwt.PyJWTError("Invalid token")
        
        result = auth_service._verify_token("invalid_token")
        
        assert result is None

    def test_get_user_by_username_found(self, auth_service, mock_user):
        """Test _get_user_by_username when user exists."""
        auth_service.session.query.return_value.filter.return_value.first.return_value = mock_user
        
        result = auth_service._get_user_by_username("testuser")
        
        assert result == mock_user
        auth_service.session.query.assert_called_with(User)

    def test_get_user_by_username_not_found(self, auth_service):
        """Test _get_user_by_username when user doesn't exist."""
        auth_service.session.query.return_value.filter.return_value.first.return_value = None
        
        result = auth_service._get_user_by_username("nonexistent")
        
        assert result is None

    def test_get_user_by_email_found(self, auth_service, mock_user):
        """Test _get_user_by_email when user exists."""
        auth_service.session.query.return_value.filter.return_value.first.return_value = mock_user
        
        result = auth_service._get_user_by_email("test@example.com")
        
        assert result == mock_user
        auth_service.session.query.assert_called_with(User)

    def test_get_user_by_email_not_found(self, auth_service):
        """Test _get_user_by_email when user doesn't exist."""
        auth_service.session.query.return_value.filter.return_value.first.return_value = None
        
        result = auth_service._get_user_by_email("nonexistent@example.com")
        
        assert result is None

    @patch.object(AuthService, '_verify_token')
    @patch.object(AuthService, '_get_user_by_username')
    def test_get_user_by_access_token_success(self, mock_get_user, mock_verify_token, auth_service, mock_user):
        """Test get_user_by_access_token with valid token."""
        mock_verify_token.return_value = {"sub": "testuser"}
        mock_get_user.return_value = mock_user
        
        result = auth_service.get_user_by_access_token("valid_token")
        
        assert result == mock_user
        mock_verify_token.assert_called_once_with("valid_token")
        mock_get_user.assert_called_once_with("testuser")

    @patch.object(AuthService, '_verify_token')
    def test_get_user_by_access_token_invalid_token(self, mock_verify_token, auth_service):
        """Test get_user_by_access_token with invalid token."""
        mock_verify_token.return_value = None
        
        result = auth_service.get_user_by_access_token("invalid_token")
        assert result is None

    @patch.object(AuthService, '_get_user_by_username')
    def test_authenticate_user_success(self, mock_get_user, auth_service, mock_user, mock_bcrypt_context):
        """Test authenticate_user with valid credentials."""
        mock_hash, mock_verify = mock_bcrypt_context
        mock_get_user.return_value = mock_user
        mock_verify.return_value = True
        
        result = auth_service.authenticate_user("testuser", "password123")
        
        assert result == mock_user
        mock_get_user.assert_called_once_with("testuser")
        mock_verify.assert_called_once_with("password123", mock_user.hashed_password)

    @patch.object(AuthService, '_get_user_by_username')
    def test_authenticate_user_user_not_found(self, mock_get_user, auth_service):
        """Test authenticate_user when user doesn't exist."""
        mock_get_user.return_value = None
        
        result = auth_service.authenticate_user("nonexistent", "password123")
        
        assert result is None

    @patch.object(AuthService, '_get_user_by_username')
    def test_authenticate_user_wrong_password(self, mock_get_user, auth_service, mock_user, mock_bcrypt_context):
        """Test authenticate_user with wrong password."""
        mock_hash, mock_verify = mock_bcrypt_context
        mock_get_user.return_value = mock_user
        mock_verify.return_value = False
        
        result = auth_service.authenticate_user("testuser", "wrongpassword")
        
        assert result is None

    @patch.object(AuthService, '_get_user_by_email')
    @patch.object(AuthService, '_get_user_by_username')
    def test_register_user_success(self, mock_get_user_by_username, mock_get_user_by_email, 
                                   auth_service, user_create_data, mock_bcrypt_context):
        """Test register_user with valid data."""
        mock_hash, mock_verify = mock_bcrypt_context
        mock_get_user_by_username.return_value = None
        mock_get_user_by_email.return_value = None
        mock_hash.return_value = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj"
        
        # Mock the created user
        mock_db_user = Mock()
        mock_db_user.id = 1
        mock_db_user.email = user_create_data.email
        mock_db_user.role = UserRoleEnum.BUYER
        mock_db_user.username = user_create_data.username
        mock_db_user.is_active = True
        mock_db_user.created_at = datetime(2024, 1, 1, 12, 0, 0)
        
        auth_service.session.refresh.side_effect = lambda user: setattr(user, 'id', 1)
        
        with patch('src.domains.auth.service.User') as mock_user_class:
            mock_user_class.return_value = mock_db_user
            
            result = auth_service.register_user(user_create_data)
            
            assert isinstance(result, UserResponse)
            assert result.email == user_create_data.email
            assert result.username == user_create_data.username
            auth_service.session.add.assert_called_once()
            auth_service.session.commit.assert_called_once()

    @patch.object(AuthService, '_get_user_by_username')
    def test_register_user_username_exists(self, mock_get_user_by_username, auth_service, 
                                           user_create_data, mock_user):
        """Test register_user when username already exists."""
        mock_get_user_by_username.return_value = mock_user
        
        with pytest.raises(HTTPException) as exc_info:
            auth_service.register_user(user_create_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already registered" in str(exc_info.value.detail)

    @patch.object(AuthService, '_get_user_by_email')
    @patch.object(AuthService, '_get_user_by_username')
    def test_register_user_email_exists(self, mock_get_user_by_username, mock_get_user_by_email,
                                        auth_service, user_create_data, mock_user):
        """Test register_user when email already exists."""
        mock_get_user_by_username.return_value = None
        mock_get_user_by_email.return_value = mock_user
        
        with pytest.raises(HTTPException) as exc_info:
            auth_service.register_user(user_create_data)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already registered" in str(exc_info.value.detail)

    @patch('src.domains.auth.service.settings')
    @patch.object(AuthService, '_create_access_token')
    @patch.object(AuthService, 'authenticate_user')
    def test_login_user_success(self, mock_authenticate, mock_create_token, mock_settings,
                                auth_service, user_login_data, mock_user):
        """Test login_user with valid credentials."""
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        mock_authenticate.return_value = mock_user
        mock_create_token.return_value = "access_token_123"
        
        result = auth_service.login_user(user_login_data)
        
        assert isinstance(result, AuthResponse)
        assert result.access_token == "access_token_123"
        assert isinstance(result.user, UserResponse)
        mock_authenticate.assert_called_once_with(user_login_data.username, user_login_data.password)

    @patch.object(AuthService, 'authenticate_user')
    def test_login_user_invalid_credentials(self, mock_authenticate, auth_service, user_login_data):
        """Test login_user with invalid credentials."""
        mock_authenticate.return_value = None
        
        with pytest.raises(HTTPException) as exc_info:
            auth_service.login_user(user_login_data)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect username or password" in str(exc_info.value.detail)
        assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}


class TestAuthServiceIntegration:
    """Integration tests for AuthService methods working together."""
    
    @patch('src.domains.auth.service.settings')
    def test_register_and_login_flow(self, mock_settings, mock_session, mock_bcrypt_context):
        """Test complete register and login flow."""
        mock_hash, mock_verify = mock_bcrypt_context
        mock_settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        mock_settings.SECRET_KEY = "test_secret"
        mock_settings.ALGORITHM = "HS256"
        mock_hash.return_value = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj"
        mock_verify.return_value = True
        
        # Setup session mocks for registration
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        # Mock the created user
        mock_db_user = Mock()
        mock_db_user.id = 1
        mock_db_user.email = "test@example.com"
        mock_db_user.username = "testuser"
        mock_db_user.is_active = True
        mock_db_user.role = "buyer"
        mock_db_user.created_at = datetime(2024, 1, 1, 12, 0, 0)
        mock_db_user.hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj"
        
        auth_service = AuthService(mock_session)
        
        # Test registration
        user_data = UserCreate(email="test@example.com", username="testuser", password="password123", role=UserRoleEnum.BUYER)
        
        with patch('src.domains.auth.service.User') as mock_user_class:
            mock_user_class.return_value = mock_db_user
            
            register_result = auth_service.register_user(user_data)
            assert isinstance(register_result, UserResponse)
            assert register_result.username == "testuser"
        
        # Setup session mocks for login (user now exists)
        mock_session.query.return_value.filter.return_value.first.return_value = mock_db_user
        
        # Test login
        login_data = UserLogin(username="testuser", password="password123")
        
        with patch.object(auth_service, '_create_access_token', return_value="test_token"):
            login_result = auth_service.login_user(login_data)
            assert isinstance(login_result, AuthResponse)
            assert login_result.access_token == "test_token"
            assert isinstance(login_result.user, UserResponse)
