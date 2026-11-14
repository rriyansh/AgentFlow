"""Initialize PostgresSaver + audit tables, then run Alembic migrations."""
import asyncio
import subprocess

from app.core.checkpointer import get_checkpointer


async def main() -> None:
    print("Initializing PostgresSaver tables...")
    get_checkpointer()
    print("Running Alembic migrations...")
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
