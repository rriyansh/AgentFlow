from app.tools.registry import registry


async def web_search(query: str) -> str:
    return f"Search results for: {query}"


registry.register("web_search", web_search)
