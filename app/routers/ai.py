from fastapi import APIRouter, Depends

from app.core.dependencies import get_chat_service
from app.schemas.schemas import UserRequest, AnalyzeResponse
from app.services.chat_service import ChatService

router = APIRouter(tags=["analyzer"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_message(
    request: UserRequest,
    service: ChatService = Depends(get_chat_service),
):
    return await service.analyze_and_save(request.message)
