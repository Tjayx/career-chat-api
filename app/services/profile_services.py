from models.user import User
from schemas.profile import ProfileExtraction


class ProfileService:

    async def update_profile(
        self,
        *,
        user: User,
        extraction: ProfileExtraction,
    ) -> bool:

        updated = False

        # Add new career interests
        for interest in extraction.new_career_interests:
            normalized_interest = interest.strip()

            if not normalized_interest:
                continue

            if normalized_interest not in user.career_interests:
                user.career_interests.append(
                    normalized_interest
                )
                updated = True

        # Add new personal interests
        for interest in extraction.new_personal_interests:
            normalized_interest = interest.strip()

            if not normalized_interest:
                continue

            if normalized_interest not in user.personal_interests:
                user.personal_interests.append(
                    normalized_interest
                )
                updated = True

        # Update years of experience
        if extraction.years_of_experience is not None:
            if (
                user.years_of_experience
                != extraction.years_of_experience
            ):
                user.years_of_experience = (
                    extraction.years_of_experience
                )
                updated = True

        return updated