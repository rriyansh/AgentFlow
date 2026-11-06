from fastapi import APIRouter

router = APIRouter()


@router.post("/run")
async def run_agent(query: str) -> dict[str, str]:
    return {"query": query, "status": "queued"}
