from app.tools.web_search import web_search
from app.tools.code_execution import execute_code

TOOLS = [web_search, execute_code]
TOOL_MAP = {t.name: t for t in TOOLS}
