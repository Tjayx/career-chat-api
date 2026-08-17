from pydantic import BaseModel, Field


class ProfileExtraction(BaseModel):
    new_career_interests: list[str] = Field(
        default_factory=list,
    )

    new_personal_interests: list[str] = Field(
        default_factory=list,
    )

    years_of_experience: int | None = None