import subprocess
import tempfile
import os
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class CodeExecutionInput(BaseModel):
    code: str = Field(description="Python code to execute")
    timeout: int = Field(default=10, ge=1, le=30, description="Timeout in seconds")


@tool("execute_code", args_schema=CodeExecutionInput)
def execute_code(code: str, timeout: int = 10) -> str:
    """Execute Python code in an isolated subprocess and return stdout/stderr."""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, dir="/tmp"
        ) as f:
            f.write(code)
            tmp_path = f.name

        result = subprocess.run(
            ["python", "-I", "-S", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            env={"PATH": "/usr/local/bin:/usr/bin:/bin", "PYTHONIOENCODING": "utf-8"},
        )
        output = result.stdout or result.stderr or "(no output)"
        return f"Exit code: {result.returncode}\nOutput:\n{output[:4000]}"
    except subprocess.TimeoutExpired:
        return f"Execution timed out after {timeout}s"
    except Exception as exc:
        return f"Execution error: {exc}"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
