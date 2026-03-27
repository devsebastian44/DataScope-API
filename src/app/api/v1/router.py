from fastapi import APIRouter
from app.api.v1.endpoints import upload, statistics, visualization


api_router = APIRouter()

api_router.include_router(
    upload.router,
    prefix="/dataset",
    tags=["Dataset Management"]
)

api_router.include_router(
    statistics.router,
    prefix="/statistics",
    tags=["Statistics"]
)

api_router.include_router(
    visualization.router,
    prefix="/visualization",
    tags=["Visualization"]
)
