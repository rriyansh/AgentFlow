from prometheus_client import Counter, Histogram

AGENT_RUNS = Counter(
    "agentflow_runs_total",
    "Total agent workflow runs",
    ["status"],
)

AGENT_LATENCY = Histogram(
    "agentflow_run_duration_seconds",
    "Agent workflow duration",
    buckets=[1, 5, 15, 30, 60, 120, 300],
)

TOOL_CALLS = Counter(
    "agentflow_tool_calls_total",
    "Total tool invocations",
    ["tool_name", "status"],
)
