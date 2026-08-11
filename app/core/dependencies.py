from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from repositories.user_repository import UserRepository
from services.auth_services import AuthService

from core.security import decode_access_token, InvalidTokenError
from repositories.conversation_repository import ConversationRepository
from services.conversation_services import ConversationService
from repositories.message_repository import MessageRepository
from services.chat_services import ChatService

from models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
http_bearer = HTTPBearer()


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(repository)


def get_conversation_service(
    db: AsyncSession = Depends(get_db),
) -> "ConversationService":
    
    repository = ConversationRepository(db)
    return ConversationService(repository)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    repository: UserRepository = Depends(get_user_repository),
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    user = await repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user

async def get_chat_service(
    conversation_service: ConversationService = Depends(get_conversation_service),
    db: AsyncSession = Depends(get_db),
    ai_client = Depends(lambda: None),  # Replace with actual AI client dependency
) -> "ChatService":
    message_repository = MessageRepository(db)
    return ChatService(
        conversation_service=conversation_service,
        message_repository=message_repository,
        ai_client=ai_client,
    )