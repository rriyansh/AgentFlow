"""Application entry point."""

from fastapi import FastAPI

from app.api.routes import agent as agent_routes
from app.api.routes import health as health_routes
from app.core.graph import build_graph
from app.core.state import AgentState

app = FastAPI(title="AgentFlow")

app.include_router(health_routes.router, tags=["health"])
app.include_router(agent_routes.router, prefix="/agent", tags=["agent"])


def main() -> None:
    graph = build_graph()
    print("AgentFlow agent initialized.")
    state = AgentState(query="Hello")
    result = graph.invoke(state)
    print(result)


if __name__ == "__main__":
    main()
