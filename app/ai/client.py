from typing import Any, TypeVar
from pydantic import BaseModel

from openai import AsyncOpenAI

from core.config import settings


T = TypeVar("T", bound=BaseModel)


class AIClient:

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

        self.model = settings.OPENAI_MODEL

    async def generate_response(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> str:

        # Prepend the system prompt to the messages
        messages = [{"role": "system", "content": system_prompt}] + messages

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "AI returned an empty response."
            )

        return content

    async def extract_profile(
        self,
        *,
        prompt: str,
        response_model: type[T],
    ) -> T:

        response = await self.client.responses.parse(
            model=self.model,
            input=prompt,
            text_format=response_model,
        )

        if response.output_parsed is None:
            raise RuntimeError(
                "AI failed to extract user profile information."
            )

        return response.output_parsed