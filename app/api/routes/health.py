from fastapi import APIRouter
from app import __version__
from app.api.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", version=__version__)


@router.get("/healthz")
async def healthz() -> dict:
    return {"status": "ok"}
