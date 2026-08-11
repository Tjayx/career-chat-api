from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    personal_interests: list[str]
    career_interests: list[str]
    years_of_experience: int | None

    onboarding_completed: bool

    model_config = ConfigDict(from_attributes=True)

