from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    
    # Database settings
    DATABASE_URL: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "team1gc_db"


    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # DodoPayments settings
    DODO_PAYMENTS_API_KEY: str = ""
    DODO_PAYMENTS_BASE_URL: str = "https://api.dodopayments.com"
    DODO_PAYMENTS_WEBHOOK_SECRET: str = ""
    
    # Frontend/Backend URLs for payment redirects
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"

    # AWS settings
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_SES_SENDER_EMAIL: str = ""


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def DEBUG(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def get_database_url(self) -> str:
        """Get the database URL. If DATABASE_URL is set, use it. Otherwise, build from components."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
