from uuid import UUID

from core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from repositories.user_repository import UserRepository
from schemas.auth import LoginRequest, RegisterRequest
from schemas.auth import TokenResponse
from models.user import User


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register(self, request: RegisterRequest) -> User:

        existing = await self.repository.get_by_email(request.email)

        if existing:
            raise ValueError("Email already exists")

        user = await self.repository.create(
            name=request.name,
            email=request.email,
            password_hash=hash_password(request.password),
            personal_interests=[],
            career_interests=[],
            years_of_experience=None,
            onboarding_completed=False,
        )

        return user

    async def login(
        self,
        request: LoginRequest,
    ) -> TokenResponse:

        user = await self.repository.get_by_email(request.email)

        if user is None:
            raise ValueError("Invalid credentials")

        if not verify_password(
            request.password,
            user.password_hash,
        ):
            raise ValueError("Invalid credentials")

        token = create_access_token(
            subject=str(user.id),
        )

        return TokenResponse(
            access_token=token,
        )

    async def get_user(
        self,
        user_id: UUID,
    ) -> User | None:

        return await self.repository.get_by_id(user_id)