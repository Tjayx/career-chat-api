from uuid import UUID

from models.message import MessageRole
from repositories.message_repository import MessageRepository
from services.conversation_services import ConversationService
from schemas.message import ChatResponse
from ai.client import AIClient
from ai.prompts import build_system_prompt


class ChatService:

    def __init__(
        self,
        conversation_service: ConversationService,
        message_repository: MessageRepository,
        ai_client: AIClient,
    ):
        self.conversation_service = conversation_service
        self.message_repository = message_repository
        self.ai_client = ai_client

    async def chat(
        self,
        *,
        conversation_id: UUID,
        user_id: UUID,
        message: str,
    ) -> ChatResponse:

        # 1. Verify that the conversation belongs to the user
        conversation = await self.conversation_service.get_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        # 2. Save the user's message
        user_message = await self.message_repository.create(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=message,
        )

        # 3. Load recent conversation history
        history = await self.message_repository.get_recent_messages(
            conversation_id=conversation.id,
            limit=20,
        )

        user = conversation.user

        system_prompt = build_system_prompt(
            career_interests=user.career_interests,
            personal_interests=user.personal_interests,
            years_of_experience=user.years_of_experience,
        )

        ai_messages = [
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in history
        ]

        # 4. Generate AI response
        ai_response = await self.ai_client.generate_response(
            system_prompt=system_prompt,
            messages=ai_messages,
        )

        # 5. Save AI response
        assistant_message = await self.message_repository.create(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=ai_response,
        )

        # 6. Return API response
        return ChatResponse(
            conversation_id=conversation.id,
            user_message_id=user_message.id,
            assistant_message_id=assistant_message.id,
            response=ai_response,
            profile_updated=False,
        )