from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CORTEXA"
    API_V1_STR: str = "/api/v1"
    
    # DATABASE
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "cortexa"
    DATABASE_URL: Optional[str] = None

    # REDIS
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # GEMINI
    GEMINI_API_KEY: Optional[str] = None

    # SECURITY
    SECRET_KEY: str = "configure-me-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.DATABASE_URL:
            url = self.DATABASE_URL
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif url.startswith("postgresql://") and "+asyncpg" not in url:
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            
            # Fix sslmode -> ssl for asyncpg
            if "sslmode=require" in url:
                url = url.replace("sslmode=require", "ssl=require")
            
            # Remove channel_binding (unsupported by asyncpg URL kwargs)
            if "channel_binding" in url:
                # Simple removal of the param and preceding/following &
                url = url.replace("&channel_binding=require", "")
                url = url.replace("?channel_binding=require", "?") # in case it's the first param

            return url
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"

settings = Settings()
