"""Tool registry."""
from app.tools.code_execution import execute_code
from app.tools.web_search import web_search

TOOLS = [web_search, execute_code]
TOOL_MAP = {t.name: t for t in TOOLS}
