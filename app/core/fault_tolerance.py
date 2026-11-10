# Retry policies & timeoutsfrom langgraph.types import RetryPolicy
from langgraph.errors import NodeTimeoutError
from app.config import settings


def get_retry_policy() -> RetryPolicy:
    """Standard retry policy for transient failures (network, rate limits)."""
    return RetryPolicy(
        initial_interval=1.0,
        backoff_factor=2.0,
        max_interval=30.0,
        max_attempts=settings.max_retry_attempts,
        jitter=True,
        retry_on=[
            ConnectionError,
            TimeoutError,
            # OpenAI rate-limit errors can be added via exception type
        ],
    )


def get_node_timeout() -> float:
    """Per-node timeout in seconds."""
    return float(settings.node_timeout_seconds)


def handle_node_failure(state: dict, error: Exception) -> dict:
    """
    Fallback error handler: records the failure and routes gracefully.
    Called only after all retries are exhausted.
    """
    return {
        "review_status": "ERROR",
        "review_feedback": f"Node failed after retries: {error!s}",
        "revision_count": state.get("revision_count", 0) + 1,
    }
