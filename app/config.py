from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "agentflow"
    debug: bool = False
    database_url: str = (
        "postgresql+psycopg://agentflow:agentflow@localhost:5432/agentflow"
    )
    langsmith_api_key: str | None = None
    langsmith_project: str | None = None
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
