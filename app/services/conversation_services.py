from uuid import UUID

from app.models.conversation import Conversation
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:

    def __init__(
        self,
        repository: ConversationRepository,
    ):
        self.repository = repository

    async def create_conversation(
        self,
        *,
        user_id: UUID,
        title: str = "New Conversation",
    ) -> Conversation:

        return await self.repository.create(
            user_id=user_id,
            title=title,
        )

    async def list_conversations(
        self,
        user_id: UUID,
    ) -> list[Conversation]:

        return await self.repository.list_by_user(
            user_id,
        )

    async def get_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> Conversation:

        conversation = await self.repository.get_by_id(
            conversation_id,
        )

        if conversation is None:
            raise ValueError("Conversation not found")

        if conversation.user_id != user_id:
            raise PermissionError(
                "You do not own this conversation."
            )

        return conversation

    async def rename_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
        title: str,
    ) -> Conversation:

        conversation = await self.get_conversation(
            conversation_id,
            user_id,
        )

        conversation.title = title

        return await self.repository.update(
            conversation,
        )

    async def delete_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> None:

        conversation = await self.get_conversation(
            conversation_id,
            user_id,
        )

        await self.repository.delete(
            conversation,
        )