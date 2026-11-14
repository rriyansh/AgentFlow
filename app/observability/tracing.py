"""OpenTelemetry tracing with LangChain auto-instrumentation."""
from functools import wraps
from typing import Any, Callable

from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.config import settings
from app.observability.logging import logger

provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint))
)
trace.set_tracer_provider(provider)
LangChainInstrumentor().instrument()

tracer = trace.get_tracer(settings.otel_service_name)


def trace_node(node_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with tracer.start_as_current_span(f"agentflow.node.{node_name}") as span:
                span.set_attribute("agentflow.node", node_name)
                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("agentflow.status", "success")
                    logger.info("node_executed", node=node_name)
                    return result
                except Exception as exc:
                    span.set_attribute("agentflow.status", "error")
                    span.record_exception(exc)
                    logger.error("node_failed", node=node_name, error=str(exc))
                    raise

        return wrapper

    return decorator
