"""Prometheus metrics."""
from prometheus_client import Counter, Histogram

AGENT_RUNS = Counter("agentflow_runs_total", "Workflow runs", ["status"])
AGENT_LATENCY = Histogram(
    "agentflow_run_duration_seconds",
    "Workflow duration",
    buckets=[1, 5, 15, 30, 60, 120, 300],
)
TOOL_CALLS = Counter(
    "agentflow_tool_calls_total", "Tool invocations", ["tool_name", "status"]
)
HTTP_REQUESTS = Counter(
    "agentflow_http_requests_total", "HTTP requests", ["method", "path", "status"]
)
HTTP_REQUEST_DURATION = Histogram(
    "agentflow_http_request_duration_seconds", "HTTP request duration", ["method"]
)
