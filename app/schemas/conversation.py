from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateConversationRequest(BaseModel):
    title: str = Field(
        default="New Conversation",
        min_length=1,
        max_length=255,
    )


class UpdateConversationRequest(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )


class ConversationResponse(BaseModel):
    id: UUID
    title: str
    summary: str | None

    created_at: datetime
    updated_at: datetime
    last_message_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )


class ConversationListResponse(BaseModel):
    conversations: list[ConversationResponse]
