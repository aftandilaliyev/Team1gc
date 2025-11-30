import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.shared.models.user import User
from src.shared.schemas.user import UserCreate, UserLogin, UserRoleEnum
from src.domains.auth.service import AuthService

# Mock the bcrypt context to prevent initialization issues during testing
@pytest.fixture(autouse=True)
def mock_bcrypt_context():
    """Mock bcrypt context to prevent initialization issues."""
    # Only mock the context initialization, not the actual methods
    # This prevents the 72-byte password error during bcrypt setup
    with patch('src.shared.models.user.pwd_context.hash') as mock_hash, \
         patch('src.shared.models.user.pwd_context.verify') as mock_verify:
        mock_hash.return_value = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj"
        mock_verify.return_value = True
        yield mock_hash, mock_verify


@pytest.fixture
def mock_session():
    """Mock database session."""
    session = Mock()
    session.query.return_value = session
    session.filter.return_value = session
    session.first.return_value = None
    session.add = Mock()
    session.commit = Mock()
    session.refresh = Mock()
    return session


@pytest.fixture
def mock_user():
    """Mock User instance."""
    user = Mock(spec=User)
    user.id = 1
    user.email = "test@example.com"
    user.username = "testuser"
    user.hashed_password = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj"
    user.is_active = True
    user.role = "buyer"
    user.created_at = datetime(2024, 1, 1, 12, 0, 0)
    return user


@pytest.fixture
def auth_service(mock_session):
    """AuthService instance with mocked session."""
    return AuthService(mock_session)


@pytest.fixture
def user_create_data():
    """Sample UserCreate data."""
    return UserCreate(
        email="newuser@example.com",
        username="newuser",
        password="password123",
        role=UserRoleEnum.BUYER,
    )


@pytest.fixture
def user_login_data():
    """Sample UserLogin data."""
    return UserLogin(
        username="testuser",
        password="password123"
    )


@pytest.fixture
def mock_jwt_payload():
    """Mock JWT payload."""
    return {
        "sub": "testuser",
        "exp": datetime(2024, 12, 31, 23, 59, 59).timestamp()
    }