from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://jobradar:jobradar_dev@localhost:5432/jobradar"
    admin_token: str = "change-me-in-production"
    cors_origins: str = "http://localhost:3000"
    app_name: str = "Job Radar API"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
