from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "GlobeTrotter"
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./globetrotter.db"
    SECRET_KEY: str = "globetrotter-hackathon-secret-key-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
