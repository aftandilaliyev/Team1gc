"""Custom exceptions for the application."""


class FileUploadError(Exception):
    """Raised when file upload fails."""
    pass


class PresignedUrlError(Exception):
    """Raised when presigned URL generation fails."""
    pass


class FileDeleteError(Exception):
    """Raised when file deletion fails."""
    pass


class ValidationError(Exception):
    """Raised when data validation fails."""
    pass


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class AuthorizationError(Exception):
    """Raised when authorization fails."""
    pass
