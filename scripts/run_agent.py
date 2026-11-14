"""Interactive CLI runner."""
import asyncio
import uuid

from langchain_core.messages import HumanMessage

from app.core.graph import app
from app.observability.logging import logger, setup_logging


async def main() -> None:
    setup_logging()
    task = input("Enter your task: ").strip()
    if not task:
        print("Task cannot be empty.")
        return

    thread_id = str(uuid.uuid4())
    state = {
        "messages": [HumanMessage(content=task)],
        "research_findings": "",
        "code_output": "",
        "review_status": "",
        "review_feedback": "",
        "revision_count": 0,
        "thread_id": thread_id,
        "user_id": "cli-user",
        "token_usage": {},
    }
    logger.info("run_started", thread_id=thread_id)
    result = await app.ainvoke(
        state, config={"configurable": {"thread_id": thread_id}}
    )
    print("\n" + "=" * 60)
    print(result["code_output"])
    print("=" * 60)
    print(f"Status: {result['review_status']} | Revisions: {result['revision_count']}")


if __name__ == "__main__":
    asyncio.run(main())
