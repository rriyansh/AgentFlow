"""Initializes the PostgreSQL checkpointer tables."""
from app.core.checkpointer import get_checkpointer


def main() -> None:
    print("Initializing PostgresSaver tables...")
    get_checkpointer()
    print("Done.")


if __name__ == "__main__":
    main()
