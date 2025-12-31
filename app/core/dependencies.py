from functools import lru_cache

from fastapi import Depends
from sqlmodel import Session

from app.core.config import GOOGLE_API_KEY
from app.db.database import get_session
from app.infra.ai_providers import GeminiClient
from app.interfaces.ai_client import AIClient
from app.services.chat_service import ChatService


@lru_cache()
def get_ai_client() -> AIClient:
    return GeminiClient(api_key=GOOGLE_API_KEY)


def get_chat_service(
    session: Session = Depends(get_session),
    ai_client: AIClient = Depends(get_ai_client),
) -> ChatService:
    return ChatService(ai_client=ai_client, session=session)
