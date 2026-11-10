"""CLI script to run AgentFlow locally."""
import asyncio
import uuid
from langchain_core.messages import HumanMessage
from app.core.graph import app
from app.observability.logging import setup_logging, logger


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

    logger.info("run_started", thread_id=thread_id, task=task)
    result = await app.ainvoke(
        state, config={"configurable": {"thread_id": thread_id}}
    )

    print("\n" + "=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    print(result["code_output"])
    print("\n" + "=" * 60)
    print(f"Status: {result['review_status']}")
    print(f"Revisions: {result['revision_count']}")
    print(f"Token usage: {result.get('token_usage')}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
