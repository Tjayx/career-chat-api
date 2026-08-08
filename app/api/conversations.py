from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import (
    get_conversation_service,
    get_current_user,
)
from app.models.user import User
from app.schemas.conversation import (
    ConversationListResponse,
    ConversationResponse,
    CreateConversationRequest,
    UpdateConversationRequest,
)
from app.services.conversation_services import ConversationService

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_conversation(
    request: CreateConversationRequest,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    return await service.create_conversation(
        user_id=current_user.id,
        title=request.title,
    )


@router.get(
    "",
    response_model=ConversationListResponse,
)
async def list_conversations(
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    conversations = await service.list_conversations(
        current_user.id
    )

    return {
        "conversations": conversations,
    }


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    try:
        return await service.get_conversation(
            conversation_id,
            current_user.id,
        )

    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    except PermissionError:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )


@router.patch(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
async def rename_conversation(
    conversation_id: UUID,
    request: UpdateConversationRequest,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    return await service.rename_conversation(
        conversation_id,
        current_user.id,
        request.title,
    )


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ConversationService = Depends(get_conversation_service),
):
    await service.delete_conversation(
        conversation_id,
        current_user.id,
    )