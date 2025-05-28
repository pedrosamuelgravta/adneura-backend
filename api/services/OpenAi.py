from openai import AsyncOpenAI
from core.exceptions import *
from core.db import SessionDep
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Literal

from core.config import get_settings
settings = get_settings()


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatOptions(BaseModel):
    model: str = "gpt-4o"
    temperature: float = 0.8
    max_tokens: int = 1000
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0


class OpenAiService:

    @staticmethod
    async def chat(system: str, assistant: str, user: str, session: SessionDep, options: ChatOptions = ChatOptions(), ) -> dict:
        try:
            openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            messages = [
                {"role": "system", "content": system},
                {"role": "assistant", "content": assistant},
                {"role": "user", "content": user},
            ]

            response = await openai.chat.completions.create(
                messages=messages,
                model=options.model,
                temperature=options.temperature,
                max_tokens=options.max_tokens,
                top_p=options.top_p,
                frequency_penalty=options.frequency_penalty,
                presence_penalty=options.presence_penalty
            )
            return response.choices[0].message.content
        except Exception as e:
            raise InternalServerError(f"OpenAI API error: {str(e)}")
