from uuid import UUID

from fastapi import APIRouter, Depends

from core.dependencies import (
    get_chat_service,
    get_current_user,
)
from models.user import User
from schemas.message import (
    ChatRequest,
    ChatResponse,
)
from services.chat_services import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/{conversation_id}",
    response_model=ChatResponse,
)
@limiter.limit("10/minute")
async def chat(
    conversation_id: UUID,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    return await service.chat(
        conversation_id=conversation_id,
        user_id=current_user.id,
        message=request.message,
    )