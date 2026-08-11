from typing import Any

from openai import AsyncOpenAI

from core.config import settings


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