from langchain_core.tools import tool


@tool
def example_tool(input_text: str) -> str:
    """An example custom tool function."""
    return f"Processed: {input_text}"
