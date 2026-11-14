"""Type-safe configuration with startup-time validation."""
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # LLM
    openai_api_key: str = Field(..., min_length=10)
    openai_model: str = "gpt-4o"

    # Database
    postgres_uri: str = Field(..., min_length=10)
    db_pool_min_size: int = Field(2, ge=1, le=50)
    db_pool_max_size: int = Field(10, ge=1, le=100)

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
    agentflow_api_key: str = Field(..., min_length=16)
    jwt_secret: str = Field(..., min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_access_ttl_minutes: int = Field(30, ge=1, le=1440)
    jwt_refresh_ttl_days: int = Field(7, ge=1, le=90)

    # CORS (comma-separated)
    cors_origins: str = "http://localhost:3000"

    # Rate limiting
    rate_limit_default: str = "60/minute"
    rate_limit_run: str = "10/minute"

    # Limits
    max_request_bytes: int = Field(1_048_576, ge=1024)  # 1 MB
    max_revisions: int = Field(3, ge=1, le=10)
    agent_timeout_seconds: int = Field(120, ge=10, le=600)
    node_timeout_seconds: int = Field(60, ge=5, le=300)
    max_retry_attempts: int = Field(3, ge=1, le=10)

    # App
    log_level: str = "INFO"
    environment: str = "development"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @model_validator(mode="after")
    def _validate_production_guardrails(self) -> "Settings":
        if self.environment == "production":
            if "*" in self.cors_origins:
                raise ValueError("CORS wildcard not allowed in production")
            if self.agentflow_api_key.startswith("change"):
                raise ValueError("Change AGENTFLOW_API_KEY before production")
            if self.jwt_secret.startswith("change"):
                raise ValueError("Change JWT_SECRET before production")
        if self.db_pool_min_size > self.db_pool_max_size:
            raise ValueError("DB_POOL_MIN_SIZE cannot exceed DB_POOL_MAX_SIZE")
        return self


settings = Settings()
