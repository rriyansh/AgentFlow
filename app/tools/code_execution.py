from app.tools.registry import registry


def code_execution(code: str) -> str:
    return f"Executed:\n{code}"


registry.register("code_execution", code_execution)
