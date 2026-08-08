from uuid import UUID

from app.models.message import Message, MessageRole
from app.repositories.message_repository import MessageRepository
from app.services.conversation_services import ConversationService


class MessageService:

    def __init__(
        self,
        repository: MessageRepository,
        conversation_service: ConversationService,
    ):
        self.repository = repository
        self.conversation_service = conversation_service

    async def create_message(
        self,
        *,
        conversation_id: UUID,
        user_id: UUID,
        role: MessageRole,
        content: str,
    ) -> Message:

        await self.conversation_service.get_conversation(
            conversation_id,
            user_id,
        )

        return await self.repository.create(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

    async def list_messages(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> list[Message]:

        await self.conversation_service.get_conversation(
            conversation_id,
            user_id,
        )

        return await self.repository.list_by_conversation(
            conversation_id,
        )