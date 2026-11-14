"""Shared FastAPI dependencies."""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import get_session
from app.domain.repositories.workflow_runs import WorkflowRunRepository
from app.security.auth import verify_api_key, verify_jwt


async def get_workflow_repo(
    session: AsyncSession = Depends(get_session),
) -> WorkflowRunRepository:
    return WorkflowRunRepository(session)


__all__ = ["verify_api_key", "verify_jwt", "get_workflow_repo"]
