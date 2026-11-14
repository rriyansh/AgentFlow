"""Retry, timeout, and fallback policies."""
from langgraph.types import RetryPolicy, TimeoutPolicy

from app.config import settings


def get_retry_policy() -> RetryPolicy:
    return RetryPolicy(
        initial_interval=1.0,
        backoff_factor=2.0,
        max_interval=30.0,
        max_attempts=settings.max_retry_attempts,
        jitter=True,
    )


def get_timeout_policy() -> TimeoutPolicy:
    return TimeoutPolicy(
        run_timeout=settings.node_timeout_seconds,
        idle_timeout=settings.node_timeout_seconds // 2,
    )


def handle_node_failure(state: dict, error: Exception) -> dict:
    return {
        "review_status": "ERROR",
        "review_feedback": f"Node failed after retries: {error!s}",
        "revision_count": state.get("revision_count", 0) + 1,
    }
