"""AI Travel Guardian+ — Health Check API"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["health"])


@router.get("/health")
async def health_check():
    """System health check endpoint."""
    from main import app_state
    return {
        "status": "ok",
        "model_loaded": app_state.get("model_loaded", False),
        "db": "connected",
        "groq": app_state.get("groq_status", "unknown"),
        "faiss": app_state.get("faiss_status", "unknown"),
    }
