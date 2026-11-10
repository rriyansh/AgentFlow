import os
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from tavily import TavilyClient

_tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))


class WebSearchInput(BaseModel):
    query: str = Field(description="The search query")
    max_results: int = Field(default=5, ge=1, le=10, description="Number of results")


@tool("web_search", args_schema=WebSearchInput)
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for current information. Use for research tasks."""
    try:
        results = _tavily.search(query=query, max_results=max_results)
        if not results.get("results"):
            return "No results found."
        return "\n\n".join(
            f"**{r['title']}**\nURL: {r['url']}\n{r['content'][:800]}"
            for r in results["results"]
        )
    except Exception as exc:
        return f"Search failed: {exc}"
