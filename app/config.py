from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # LLM
    openai_api_key: str
    openai_model: str = "gpt-4o"

    # Database
    postgres_uri: str
    db_pool_min_size: int = 2
    db_pool_max_size: int = 10

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # Tools
    tavily_api_key: str = ""

    # Observability
    langsmith_tracing: bool = True
    langsmith_api_key: str = ""
    langsmith_project: str = "agentflow"
    otel_exporter_otlp_endpoint: str = "http://jaeger:4317"
    otel_service_name: str = "agentflow"

    # Security
    agentflow_api_key: str = "dev-key"
    jwt_secret: str = "dev-secret"
    jwt_algorithm: str = "HS256"
    rate_limit_default: str = "60/minute"

    # App
    log_level: str = "INFO"
    max_revisions: int = 3
    agent_timeout_seconds: int = 120
    node_timeout_seconds: int = 60
    max_retry_attempts: int = 3


settings = Settings()
