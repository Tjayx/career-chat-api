from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.message import MessageRole


class CreateMessageRequest(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class MessageResponse(BaseModel):
    id: UUID

    role: MessageRole

    content: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class MessageListResponse(BaseModel):
    messages: list[MessageResponse]


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
    )


class ChatResponse(BaseModel):
    conversation_id: UUID

    user_message_id: UUID

    assistant_message_id: UUID

    response: str

    profile_updated: bool


class ConversationDetailResponse(BaseModel):
    id: UUID

    title: str

    summary: str | None

    created_at: datetime

    updated_at: datetime

    last_message_at: datetime | None

    messages: list[MessageResponse]

    model_config = ConfigDict(
        from_attributes=True,
    )