# <img src="https://cdn.simpleicons.org/langchain/1C3C3C" width="32" height="32" alt="LangGraph" /> AgentFlow v4

**Enterprise Multi-Agent System — Hardened, Observable, Production-Ready**

[![CI](https://github.com/your-org/agentflow/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/agentflow/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/your-org/agentflow/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/agentflow)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.4-1C3C3C.svg)](https://langchain-ai.github.io/langgraph/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)](https://redis.io/)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-instrumented-425CC7.svg)](https://opentelemetry.io/)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Security](#security)
- [Observability](#observability)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**AgentFlow v4** is a production-grade, autonomous multi-agent system that orchestrates a team of specialized AI agents — **Researcher**, **Coder**, and **Reviewer** — through a durable LangGraph state machine to execute complex, multi-step business workflows without human intervention.

Each agent is equipped with domain-specific tools, structured reasoning, and shared memory. The system self-heals from transient failures, exposes full observability, and ships with a hardened security posture (JWT + API key + rate limiting + audit trail).

### Why AgentFlow?

- **Autonomous workflows** — Agents plan, execute, review, and iterate without human touch
- **Self-healing** — Per-node retries, timeouts, and graceful fallbacks
- **Durable state** — PostgreSQL checkpointing enables crash recovery and resume
- **Multi-tenant safe** — Thread isolation per user
- **Fully observable** — OpenTelemetry traces, Prometheus metrics, structured logs, LangSmith LLM traces
- **Security first** — Dual auth, rate limiting, request size caps, CORS allowlist, secret validation

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Client / HTTP Request                    │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                   FastAPI + Middleware Stack                 │
│   (Request ID · Body Limit · CORS · Rate Limit · Auth)       │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    LangGraph StateGraph                      │
│                                                              │
│   ┌──────────────┐   ┌─────────┐   ┌──────────┐              │
│   │  Researcher  │──▶│  Coder  │──▶│ Reviewer │              │
│   │ (web_search) │   │(execute)│   │(structured)│            │
│   └──────────────┘   └─────────┘   └──────────┘              │
│          ▲               │               │                   │
│          │               │   NEEDS_REVISION                  │
│          │               └───────────────┘                   │
│          │                            │ APPROVED             │
│          │                            ▼                      │
│          │                           END                     │
│          │                                                   │
│          └── PostgresSaver (durable checkpointer)            │
└───────────────────────────┬──────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   PostgreSQL           Redis              Jaeger / OTel
  (state + audit)   (rate limiting)     (distributed traces)
```

### Workflow Flow

1. **Researcher** receives the task, performs web search, returns structured findings.
2. **Coder** uses the findings to write production-quality code and verifies it via sandboxed execution.
3. **Reviewer** audits the code with structured output (`APPROVED` or `NEEDS_REVISION` + feedback).
4. On `NEEDS_REVISION`, the graph loops back to **Coder** (bounded by `MAX_REVISIONS`).
5. On `APPROVED`, the workflow completes and returns the final artifact.

Every node has **retries**, **timeouts**, and an **error handler** — transient failures don't kill the workflow.

---

## Features

| Capability | Implementation |
|---|---|
| Self-Healing | Per-node `RetryPolicy` with exponential backoff + jitter |
| Never Hangs | `TimeoutPolicy` per node attempt |
| Graceful Degradation | `error_handler` runs after retries exhausted |
| Durable State | PostgreSQL `PostgresSaver` with connection pooling |
| Multi-Tenant Safe | `thread_id` scoped per `user_id` |
| Dual Authentication | API key (`x-api-key`) + JWT Bearer |
| JWT Revocation | Redis-backed JTI blacklist |
| Distributed Rate Limiting | SlowAPI + Redis (moving window, user-aware) |
| Request Body Limit | Middleware-enforced (default 1 MB) |
| CORS Allowlist | Config-driven; wildcard rejected in production |
| Secret Validation | `Settings` fails fast on weak secrets in production |
| Audit Trail | `workflow_runs` table with duration + revisions |
| Real-Time Streaming | Server-Sent Events via `astream_events(v2)` |
| Full Observability | OpenTelemetry + Prometheus + structlog + LangSmith |
| Structured Errors | `ErrorEnvelope` with request ID correlation |
| Production Docker | Multi-stage, non-root user, healthchecks |
| Comprehensive Tests | Graph, API, auth, fault tolerance, errors |

---

## Tech Stack

<p align="left">
  <img src="https://cdn.simpleicons.org/python/3776AB" width="40" height="40" alt="Python" />
  <img src="https://cdn.simpleicons.org/fastapi/009688" width="40" height="40" alt="FastAPI" />
  <img src="https://cdn.simpleicons.org/langchain/1C3C3C" width="40" height="40" alt="LangChain" />
  <img src="https://cdn.simpleicons.org/openai/412991" width="40" height="40" alt="OpenAI" />
  <img src="https://cdn.simpleicons.org/postgresql/4169E1" width="40" height="40" alt="PostgreSQL" />
  <img src="https://cdn.simpleicons.org/redis/DC382D" width="40" height="40" alt="Redis" />
  <img src="https://cdn.simpleicons.org/docker/2496ED" width="40" height="40" alt="Docker" />
  <img src="https://cdn.simpleicons.org/opentelemetry/425CC7" width="40" height="40" alt="OpenTelemetry" />
  <img src="https://cdn.simpleicons.org/prometheus/E6522C" width="40" height="40" alt="Prometheus" />
  <img src="https://cdn.simpleicons.org/githubactions/2088FF" width="40" height="40" alt="GitHub Actions" />
  <img src="https://cdn.simpleicons.org/pydantic/E92063" width="40" height="40" alt="Pydantic" />
</p>

| Layer | Technology |
|---|---|
| **Orchestration** | LangGraph (`StateGraph`, `RetryPolicy`, `TimeoutPolicy`) |
| **LLM** | OpenAI GPT-4o via LangChain |
| **API Framework** | FastAPI + Uvicorn |
| **Persistence** | PostgreSQL 16 (`PostgresSaver` + SQLAlchemy async) |
| **Cache / Rate Limit** | Redis 7 |
| **Migrations** | Alembic |
| **Observability** | OpenTelemetry + Prometheus + structlog + LangSmith |
| **Security** | PyJWT + SlowAPI + APIKeyHeader |
| **Testing** | Pytest + pytest-asyncio + httpx |
| **CI/CD** | GitHub Actions |
| **Packaging** | uv + `pyproject.toml` |
| **Containerization** | Docker multi-stage + Docker Compose |

---

## Project Structure

```
agentflow/
│
├── .github/workflows/
│   ├── ci.yml                         # Lint + test + coverage
│   └── deploy.yml                     # LangSmith deploy
│
├── app/
│   ├── __init__.py                    # Version
│   ├── main.py                        # FastAPI app + middleware + handlers
│   ├── config.py                      # Pydantic settings with validators
│   │
│   ├── core/                          # Orchestration layer
│   │   ├── state.py                   # Shared TypedDict state
│   │   ├── graph.py                   # StateGraph definition
│   │   ├── routing.py                 # Conditional edges
│   │   ├── checkpointer.py            # PostgresSaver singleton
│   │   ├── fault_tolerance.py         # Retry + timeout policies
│   │   ├── exceptions.py              # Custom exception hierarchy
│   │   ├── middleware.py              # Request ID + body limit + metrics
│   │   └── lifespan.py                # Startup/shutdown orchestration
│   │
│   ├── agents/                        # Specialized agents
│   │   ├── base.py                    # BaseAgent ABC
│   │   ├── researcher.py              # Web-search agent
│   │   ├── coder.py                   # Code-writing agent
│   │   └── reviewer.py                # Structured-output reviewer
│   │
│   ├── tools/                         # Agent tools
│   │   ├── web_search.py              # Tavily search
│   │   ├── code_execution.py          # Sandboxed subprocess runner
│   │   └── registry.py                # Tool registry
│   │
│   ├── api/                           # FastAPI layer
│   │   ├── schemas.py                 # Request/response models
│   │   ├── dependencies.py            # Shared dependencies
│   │   ├── rate_limit.py              # SlowAPI limiter
│   │   └── routes/
│   │       ├── health.py              # /health, /healthz, /readyz, /metrics
│   │       ├── agent.py               # /v1/agent/run, /state
│   │       ├── stream.py              # /v1/agent/stream (SSE)
│   │       └── auth.py                # /v1/auth/token, /refresh
│   │
│   ├── domain/                        # Business layer
│   │   └── repositories/
│   │       └── workflow_runs.py       # Audit trail repository
│   │
│   ├── db/                            # Database layer
│   │   ├── engine.py                  # Async SQLAlchemy engine
│   │   └── models.py                  # ORM models
│   │
│   ├── observability/                 # Logging + tracing + metrics
│   │   ├── logging.py                 # structlog JSON
│   │   ├── tracing.py                 # OpenTelemetry setup
│   │   └── metrics.py                 # Prometheus counters/histograms
│   │
│   └── security/                      # Auth
│       ├── auth.py                    # FastAPI dependencies
│       └── jwt_handler.py             # Issue / verify / revoke
│
├── migrations/                        # Alembic
│   ├── env.py
│   ├── script.py.mako
│   └── versions/0001_initial.py
│
├── tests/
│   ├── conftest.py
│   ├── test_graph.py
│   ├── test_api.py
│   ├── test_auth.py
│   ├── test_errors.py
│   ├── test_nodes.py
│   └── test_fault_tolerance.py
│
├── scripts/
│   ├── seed_db.py                     # Init PostgresSaver + migrations
│   └── run_agent.py                   # CLI runner
│
├── monitoring/
│   └── prometheus.yml                 # Scrape config
│
├── .env.example                       # Environment template
├── .gitignore
├── .dockerignore
├── .editorconfig
├── Dockerfile                         # Production multi-stage
├── Dockerfile.dev                     # Dev with hot reload
├── docker-compose.yml                 # Production stack
├── docker-compose.dev.yml             # Dev stack
├── alembic.ini
├── langgraph.json                     # LangGraph CLI config
├── pyproject.toml                     # Deps + tooling
├── Makefile                           # Dev shortcuts
├── README.md
└── LICENSE
```

---

## Prerequisites

| Requirement | Version | Purpose |
|---|---|---|
| Python | 3.12+ | Runtime |
| Docker | 24+ | Containerization |
| Docker Compose | 2.20+ | Multi-service orchestration |
| OpenAI API Key | — | LLM access |
| Tavily API Key | — | Web search (optional) |
| uv | Latest | Python package manager (recommended) |

---

## Installation

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-org/agentflow.git
cd agentflow
```

### Step 2 — Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and fill in required secrets:

```env
OPENAI_API_KEY=sk-your-real-openai-key
TAVILY_API_KEY=tvly-your-real-tavily-key
AGENTFLOW_API_KEY=generate-a-32-char-random-string
JWT_SECRET=generate-a-64-char-random-string
```

### Step 3 — Start the Stack

**Production mode:**

```bash
docker compose up --build -d
```

**Development mode (hot reload):**

```bash
docker compose -f docker-compose.dev.yml up --build
```

### Step 4 — Verify

```bash
curl http://localhost:8000/health
# Expected: {"status":"ok","version":"4.0.0"}
```

### Step 5 — Initialize Database

```bash
docker compose exec agentflow-api python scripts/seed_db.py
```

---

## Configuration

All configuration is environment-driven. See `.env.example` for full template.

### Required Variables

| Variable | Description | Example |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `POSTGRES_URI` | PostgreSQL connection string | `postgresql://postgres:postgres@postgres:5432/agentflow` |
| `AGENTFLOW_API_KEY` | API key for client authentication | 32+ char random string |
| `JWT_SECRET` | JWT signing secret | 64+ char random string |

### Optional Variables

| Variable | Default | Description |
|---|---|---|
| `OPENAI_MODEL` | `gpt-4o` | LLM model name |
| `TAVILY_API_KEY` | `""` | Tavily search API key |
| `REDIS_URL` | `redis://redis:6379/0` | Redis URL for rate limiting |
| `LANGSMITH_TRACING` | `true` | Enable LangSmith traces |
| `LANGSMITH_API_KEY` | `""` | LangSmith API key |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://jaeger:4317` | OTel collector endpoint |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowlist |
| `RATE_LIMIT_DEFAULT` | `60/minute` | Global rate limit |
| `RATE_LIMIT_RUN` | `10/minute` | Agent run rate limit |
| `MAX_REQUEST_BYTES` | `1048576` | Request body size cap (1 MB) |
| `MAX_REVISIONS` | `3` | Max review→code loops |
| `NODE_TIMEOUT_SECONDS` | `60` | Per-node wall clock timeout |
| `MAX_RETRY_ATTEMPTS` | `3` | Max retries per node |
| `JWT_ACCESS_TTL_MINUTES` | `30` | Access token TTL |
| `JWT_REFRESH_TTL_DAYS` | `7` | Refresh token TTL |
| `LOG_LEVEL` | `INFO` | Log verbosity |
| `ENVIRONMENT` | `development` | `development` / `production` |

### Secret Generation

```bash
# Generate strong secrets
python -c "import secrets; print(secrets.token_urlsafe(32))"   # API key
python -c "import secrets; print(secrets.token_urlsafe(64))"   # JWT secret
```

---

## Usage

### Run a Workflow (Synchronous)

```bash
curl -X POST http://localhost:8000/v1/agent/run \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-agentflow-api-key" \
  -d '{
    "task": "Write a Python token bucket rate limiter and test it with 5 scenarios.",
    "user_id": "user-123"
  }'
```

**Response:**

```json
{
  "thread_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "APPROVED",
  "final_output": "```python\nimport time\n\nclass TokenBucket:\n    ...\n```",
  "revisions": 1,
  "token_usage": {
    "researcher": {"input_tokens": 320, "output_tokens": 180},
    "coder": {"input_tokens": 890, "output_tokens": 640}
  }
}
```

### Stream Events (SSE)

```bash
curl -N -X POST http://localhost:8000/v1/agent/stream \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-agentflow-api-key" \
  -d '{"task": "Write a Python email validator"}'
```

**Stream output:**

```
event: node_start
data: {"node": "researcher"}

event: node_end
data: {"node": "researcher"}

event: node_start
data: {"node": "coder"}

event: node_end
data: {"node": "coder"}

event: node_start
data: {"node": "reviewer"}

event: node_end
data: {"node": "reviewer"}
```

### Inspect Thread State

```bash
curl "http://localhost:8000/v1/agent/state/a1b2c3d4-e5f6-7890-abcd-ef1234567890?user_id=user-123" \
  -H "x-api-key: your-agentflow-api-key"
```

### Issue JWT Tokens

```bash
curl -X POST http://localhost:8000/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"subject": "user-123", "scopes": ["read", "write"]}'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 1800
}
```

### Refresh Access Token

```bash
curl -X POST http://localhost:8000/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "your-refresh-token"}'
```

### CLI Runner

```bash
make run-agent
```

---

## API Reference

### Endpoints Overview

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/health` | None | Liveness with version |
| `GET` | `/healthz` | None | Kubernetes liveness probe |
| `GET` | `/readyz` | None | Readiness (Postgres + Redis ping) |
| `GET` | `/metrics` | None | Prometheus scrape endpoint |
| `POST` | `/v1/auth/token` | None* | Issue access + refresh tokens |
| `POST` | `/v1/auth/refresh` | None | Refresh access token |
| `POST` | `/v1/agent/run` | `x-api-key` | Execute workflow synchronously |
| `POST` | `/v1/agent/stream` | `x-api-key` | Stream node events (SSE) |
| `GET` | `/v1/agent/state/{thread_id}` | `x-api-key` | Inspect thread state |

*In production, protect `/v1/auth/token` behind your identity provider.

### POST /v1/agent/run

**Request Body:**

```json
{
  "task": "string (1-4000 chars)",
  "thread_id": "string (optional, resume existing)",
  "user_id": "string (default: 'default')"
}
```

**Rate Limit:** `10/minute` per authenticated principal.

**Error Response Format:**

```json
{
  "error": {
    "code": "authentication_error",
    "message": "Invalid or missing API key",
    "details": {},
    "request_id": "abc-123-def-456"
  }
}
```

**HTTP Status Codes:**

| Code | Meaning |
|---|---|
| `200` | Success |
| `401` | Authentication failed |
| `413` | Payload too large |
| `422` | Validation error |
| `429` | Rate limit exceeded |
| `500` | Internal error |
| `502` | Upstream (LLM/tool) failure |
| `503` | Service unavailable |

### Interactive API Docs

FastAPI auto-generates interactive docs:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

---

## Security

### Authentication

- **API key** (`x-api-key` header) for service-to-service calls
- **JWT Bearer** for user-scoped access
- **JWT revocation** via Redis JTI blacklist
- **Short-lived access tokens** (30 min default) + refresh tokens (7 days)

### Application Security

- **Strict input validation** via Pydantic
- **Request body size cap** (1 MB default) enforced in middleware
- **CORS allowlist** — wildcard explicitly rejected in production
- **Rate limiting** — Redis-backed moving window, keyed per user/IP
- **Secure error envelopes** — internal details never leak to clients
- **Secret validation at startup** — `Settings` fails fast on weak secrets in production

### Sandboxed Code Execution

- Subprocess isolation (`python -I -S`)
- Strict env allowlist (only `PATH` and `PYTHONIOENCODING`)
- Hard wall-clock timeout (default 10s, configurable 1-30s)
- Temp files cleaned up in `finally` block

### Infrastructure Security

- **Non-root Docker user** (`appuser`, uid 1000)
- **Multi-stage builds** — no build tools in runtime image
- **Health checks** on all containers
- **No secrets in images** — all via env at runtime
- **Graceful shutdown** — in-flight requests drained before exit

### Secret Rotation Checklist

- [ ] Rotate `AGENTFLOW_API_KEY` and `JWT_SECRET` before production
- [ ] Set `ENVIRONMENT=production` (enables strict validation)
- [ ] Restrict `CORS_ORIGINS` to known hosts only
- [ ] Enable HTTPS via reverse proxy
- [ ] Run `alembic upgrade head` on every deploy

---

## Observability

### Distributed Traces (Jaeger)

Every node execution and LLM call is traced via OpenTelemetry.

**Access:** `http://localhost:16686`

**Filter by:** `service.name = agentflow`

**Captures:**

- Node execution duration
- LLM token usage per call
- Retry attempts
- Error paths with stack traces

### Metrics (Prometheus)

**Access:** `http://localhost:9090` (Prometheus UI) · `http://localhost:8000/metrics` (raw scrape)

**Key metrics:**

| Metric | Type | Description |
|---|---|---|
| `agentflow_runs_total` | Counter | Workflow runs by status |
| `agentflow_run_duration_seconds` | Histogram | End-to-end workflow latency |
| `agentflow_tool_calls_total` | Counter | Tool invocations by name + status |
| `agentflow_http_requests_total` | Counter | HTTP requests by method/path/status |
| `agentflow_http_request_duration_seconds` | Histogram | HTTP request latency |

**Sample Prometheus alerts to configure:**

```yaml
- alert: HighErrorRate
  expr: rate(agentflow_http_requests_total{status=~"5.."}[5m]) > 0.05
  for: 5m

- alert: SlowWorkflows
  expr: histogram_quantile(0.95, agentflow_run_duration_seconds_bucket) > 120
  for: 10m
```

### LLM Traces (LangSmith)

Set `LANGSMITH_API_KEY` in `.env` and view traces at [smith.langchain.com](https://smith.langchain.com/).

**Captures:**

- Full prompt/response pairs
- Chain execution tree
- Cost per run
- Token usage breakdown

### Structured Logs

JSON logs to stdout via `structlog`. Ideal for `docker logs`, Loki, Datadog, or ELK.

**Example log line:**

```json
{
  "event": "http_request",
  "method": "POST",
  "path": "/v1/agent/run",
  "status": 200,
  "duration_ms": 8421.33,
  "request_id": "abc-123-def-456",
  "level": "info",
  "timestamp": "2026-11-14T12:34:56.789Z"
}
```

---

## Testing

### Run All Tests

```bash
make test
```

### Individual Test Suites

```bash
# Graph routing logic
uv run pytest tests/test_graph.py -v

# API endpoints + auth
uv run pytest tests/test_api.py -v

# JWT issue / verify / revoke
uv run pytest tests/test_auth.py -v

# Fault tolerance (retry + timeout)
uv run pytest tests/test_fault_tolerance.py -v

# Error envelope format
uv run pytest tests/test_errors.py -v
```

### Coverage

```bash
uv run pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Test Strategy

- **Unit tests** use `MemorySaver` (no Postgres required)
- **Integration tests** (API) use `httpx.AsyncClient` + `ASGITransport`
- **Fault tolerance tests** simulate transient failures + timeouts
- **Auth tests** verify JWT lifecycle + revocation
- **Error tests** validate the envelope format

All tests run in under 10 seconds with no external dependencies.

---

## Docker Deployment

### Full Stack Commands

```bash
# Build images
docker compose build

# Start all services (detached)
docker compose up -d

# Check status
docker compose ps

# Follow logs
docker compose logs -f

# Follow logs for a specific service
docker compose logs -f agentflow-api

# Stop and remove containers
docker compose down

# Stop and remove volumes (destroys data)
docker compose down -v
```

### Service Ports

| Service | Port | Purpose |
|---|---|---|
| AgentFlow API | `8000` | Main API |
| PostgreSQL | `5432` | Database |
| Redis | `6379` | Rate limiting |
| Jaeger UI | `16686` | Tracing UI |
| Jaeger OTLP | `4317` | Trace collection |
| Prometheus | `9090` | Metrics UI |

### Rebuild After Code Changes

```bash
# Fast rebuild (reuses cache)
docker compose up --build -d agentflow-api

# Full rebuild (no cache)
docker compose build --no-cache agentflow-api
docker compose up -d agentflow-api
```

### Run Migrations

```bash
docker compose exec agentflow-api alembic upgrade head
```

### Inspect Container Errors

```bash
# View last 200 log lines
docker compose logs --tail=200 agentflow-api

# Shell into the container
docker compose exec agentflow-api /bin/bash

# Check health status
docker compose ps
```

### Clean Up Unused Resources

```bash
# Remove stopped containers + unused networks
docker system prune -f

# Also remove unused images
docker system prune -a -f

# Also remove volumes (DESTROYS DATA)
docker system prune -a -f --volumes
```

### Development Stack (Hot Reload)

```bash
docker compose -f docker-compose.dev.yml up --build
```

The `app/` directory is mounted as a volume, so code changes trigger auto-reload.

---

## Production Deployment

### Option 1 — LangSmith Cloud (Recommended)

Fully managed, auto-scaling, built-in observability.

```bash
pip install -U "langgraph-cli[inmem]"
langgraph deploy \
  --agent-id agentflow \
  --agent-environment production
```

Set these secrets in your LangSmith dashboard:

- `OPENAI_API_KEY`
- `POSTGRES_URI`
- `TAVILY_API_KEY`
- `AGENTFLOW_API_KEY`
- `JWT_SECRET`

### Option 2 — Self-Hosted Docker

```bash
docker compose up --build -d
```

Add in front:

- **Reverse proxy** (nginx / Caddy / Traefik) for HTTPS + TLS termination
- **Log aggregation** (Loki / CloudWatch / Datadog)
- **Postgres backups** (daily snapshots)

### Option 3 — Kubernetes

Use the LangSmith Helm chart:

```bash
helm repo add langchain https://langchain-ai.github.io/helm/
helm install agentflow langchain/langgraph-cloud \
  --set config.postgresUri=$POSTGRES_URI \
  --set config.openaiApiKey=$OPENAI_API_KEY
```

### Production Checklist

- [ ] Set `ENVIRONMENT=production`
- [ ] Rotate `AGENTFLOW_API_KEY` and `JWT_SECRET`
- [ ] Restrict `CORS_ORIGINS` to known origins
- [ ] Enable HTTPS (reverse proxy + valid certificates)
- [ ] Set `LOG_LEVEL=WARNING` to reduce noise
- [ ] Configure log aggregation pipeline
- [ ] Set up Prometheus alerts on error rate + latency
- [ ] Verify Postgres backups + point-in-time recovery
- [ ] Enable `LANGSMITH_TRACING=true` for LLM debugging
- [ ] Run `alembic upgrade head` on deploy
- [ ] Gate `/v1/auth/token` behind your IdP or remove in production
- [ ] Configure resource limits in Docker Compose / K8s
- [ ] Set up uptime monitoring on `/healthz`

---

## Troubleshooting

### `docker compose up` fails on `agentflow-api`

**Cause:** Postgres not ready.

**Fix:**

```bash
docker compose down -v
docker compose up --build
```

### `psycopg.OperationalError: connection refused`

**Cause:** `POSTGRES_URI` uses `localhost` instead of `postgres` (Docker service name).

**Fix:** Inside Docker:

```env
POSTGRES_URI=postgresql://postgres:postgres@postgres:5432/agentflow
```

Outside Docker (local dev):

```env
POSTGRES_URI=postgresql://postgres:postgres@localhost:5432/agentflow
```

### `401 Unauthorized` from `/v1/agent/run`

**Cause:** Missing or wrong `x-api-key`.

**Fix:**

```bash
curl -H "x-api-key: $(grep AGENTFLOW_API_KEY .env | cut -d= -f2)" ...
```

### `413 Payload Too Large`

**Cause:** Request body exceeds `MAX_REQUEST_BYTES` (default 1 MB).

**Fix:** Either reduce the payload or increase `MAX_REQUEST_BYTES` in `.env`.

### `429 Too Many Requests`

**Cause:** Rate limit hit (`10/minute` for `/v1/agent/run`, `60/minute` globally).

**Fix:** Adjust `RATE_LIMIT_DEFAULT` / `RATE_LIMIT_RUN` in `.env`, or wait for the window to reset.

### Reviewer always returns `NEEDS_REVISION`

**Cause:** Task too vague, or the coder is stuck on a bug.

**Fix:**

- Make the `task` more specific
- Inspect intermediate state: `GET /v1/agent/state/{thread_id}`
- Set `MAX_REVISIONS=1` in dev to fail faster

### `ModuleNotFoundError` inside container

**Cause:** New dependency missing from `pyproject.toml`.

**Fix:**

```bash
uv add <package>
docker compose build --no-cache agentflow-api
docker compose up -d agentflow-api
```

### LangGraph checkpoint tables missing

**Cause:** `PostgresSaver.setup()` hasn't run.

**Fix:**

```bash
docker compose exec agentflow-api python scripts/seed_db.py
```

### Alembic migration fails

**Cause:** `POSTGRES_URI` points to wrong DB or DB not ready.

**Fix:**

```bash
docker compose exec postgres pg_isready -U postgres
docker compose exec agentflow-api alembic current
docker compose exec agentflow-api alembic upgrade head
```

### `/readyz` returns `degraded`

**Cause:** One or more dependencies (Postgres or Redis) unreachable.

**Fix:** Check the `checks` object in the response:

```bash
curl http://localhost:8000/readyz | jq
```

---

## Contributing

Contributions welcome! Follow these steps:

### 1. Fork and Branch

```bash
git checkout -b feat/your-feature-name
```

### 2. Install Dev Dependencies

```bash
make install
```

### 3. Make Changes

Write code + tests. Ensure tests pass:

```bash
make lint
make test
```

### 4. Commit (Conventional Commits)

```
feat(agents): add a DataAnalyst agent
fix(routing): handle empty feedback
docs(readme): add Kubernetes example
```

### 5. Open a Pull Request

CI must pass before review. Include tests for new features.

### Code Style

| Rule | Standard |
|---|---|
| Line length | 100 chars |
| Type checking | `mypy --strict` |
| Formatting | `ruff format` |
| Linting | `ruff check` |
| Tests | Every feature needs tests |

### Ideas for Contributors

- **Human-in-the-loop** — `interrupt()` before Coder for manual approval
- **Sub-agents** — Parallel researcher agents for faster info gathering
- **Long-term memory** — Mem0 / Qdrant integration for cross-session learning
- **Multi-language** — Translator agent for i18n pipelines
- **Cost budgets** — Per-thread token caps with alerts
- **Custom evaluators** — Automated quality scoring with LangSmith datasets
- **OpenAPI SDK** — Auto-generated TypeScript/Python clients

---

## Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) — stateful multi-agent orchestration
- [LangSmith](https://smith.langchain.com/) — production LLM tracing
- [FastAPI](https://fastapi.tiangolo.com/) — modern async web framework
- [SlowAPI](https://github.com/laurentS/slowapi) — simple rate limiting
- [OpenTelemetry](https://opentelemetry.io/) — vendor-neutral observability
- [structlog](https://www.structlog.org/) — structured logging

---

## License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for full text.

**TL;DR:** Free for personal and commercial use. Keep the copyright notice.



<sub>If AgentFlow saved you time, consider giving it a <a href="https://github.com/your-org/agentflow">star</a>.</sub>

</div>
