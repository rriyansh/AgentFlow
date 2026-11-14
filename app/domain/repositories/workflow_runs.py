"""Repository for workflow audit trail."""
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import WorkflowRun


class WorkflowRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        thread_id: str,
        user_id: str,
        task: str,
        status: str,
        revisions: int,
        duration_ms: int | None = None,
    ) -> WorkflowRun:
        run = WorkflowRun(
            thread_id=thread_id,
            user_id=user_id,
            task=task[:4000],
            status=status,
            revisions=revisions,
            duration_ms=duration_ms,
        )
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run
