from uuid import UUID

from ai.client import AIClient
from ai.profile_extractor import ProfileExtractor
from ai.prompts import build_system_prompt
from models.message import MessageRole
from repositories.message_repository import MessageRepository
from schemas.message import ChatResponse
from services.conversation_services import ConversationService
from services.profile_services import ProfileService


class ChatService:

    def __init__(
        self,
        conversation_service: ConversationService,
        message_repository: MessageRepository,
        ai_client: AIClient,
        profile_extractor: ProfileExtractor,
        profile_service: ProfileService,
    ):
        self.conversation_service = conversation_service
        self.message_repository = message_repository
        self.ai_client = ai_client
        self.profile_extractor = profile_extractor
        self.profile_service = profile_service

    async def chat(
        self,
        *,
        conversation_id: UUID,
        user_id: UUID,
        user,
        message: str,
    ) -> ChatResponse:

        # --------------------------------
        # 1. Verify conversation ownership
        # --------------------------------

        conversation = (
            await self.conversation_service.get_conversation(
                conversation_id=conversation_id,
                user_id=user_id,
            )
        )

        # --------------------------------
        # 2. Save user's message
        # --------------------------------

        user_message = (
            await self.message_repository.create(
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content=message,
            )
        )

        # --------------------------------
        # 3. Extract profile information
        # --------------------------------

        extraction = (
            await self.profile_extractor.extract(
                message=message,
                current_career_interests=(
                    user.career_interests
                ),
                current_personal_interests=(
                    user.personal_interests
                ),
                current_years_of_experience=(
                    user.years_of_experience
                ),
            )
        )

        # --------------------------------
        # 4. Update user profile
        # --------------------------------

        profile_updated = (
            await self.profile_service.update_profile(
                user=user,
                extraction=extraction,
            )
        )

        # --------------------------------
        # 5. Load conversation history
        # --------------------------------

        history = (
            await self.message_repository
            .get_recent_messages(
                conversation_id=conversation.id,
                limit=20,
            )
        )

        ai_messages = [
            {
                "role": msg.role.value,
                "content": msg.content,
            }
            for msg in history
        ]

        # --------------------------------
        # 6. Build system prompt
        # --------------------------------

        system_prompt = build_system_prompt(
            career_interests=user.career_interests,
            personal_interests=user.personal_interests,
            years_of_experience=user.years_of_experience,
        )

        # --------------------------------
        # 7. Generate AI response
        # --------------------------------

        ai_response = (
            await self.ai_client.generate_response(
                system_prompt=system_prompt,
                messages=ai_messages,
            )
        )

        # --------------------------------
        # 8. Save assistant message
        # --------------------------------

        assistant_message = (
            await self.message_repository.create(
                conversation_id=conversation.id,
                role=MessageRole.ASSISTANT,
                content=ai_response,
            )
        )

        # --------------------------------
        # 9. Return response
        # --------------------------------

        return ChatResponse(
            conversation_id=conversation.id,
            user_message_id=user_message.id,
            assistant_message_id=assistant_message.id,
            response=ai_response,
            profile_updated=profile_updated,
        )