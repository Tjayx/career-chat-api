from app.ai.client import AIClient
from app.ai.prompts import PROFILE_EXTRACTION_PROMPT
from app.schemas.profile import ProfileExtraction


class ProfileExtractor:

    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client

    async def extract(
        self,
        *,
        message: str,
        current_career_interests: list[str],
        current_personal_interests: list[str],
        current_years_of_experience: int | None,
    ) -> ProfileExtraction:

        prompt = PROFILE_EXTRACTION_PROMPT.format(
            career_interests=", ".join(
                current_career_interests
            ) or "None",
            personal_interests=", ".join(
                current_personal_interests
            ) or "None",
            years_of_experience=(
                current_years_of_experience
                if current_years_of_experience is not None
                else "Not provided"
            ),
            message=message,
        )

        return await self.ai_client.extract_profile(
            prompt=prompt,
            response_model=ProfileExtraction,
        )