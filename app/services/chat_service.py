from sqlmodel import Session

from app.interfaces.ai_client import AIClient
from app.models.ai import MessageLog
from app.schemas.schemas import AnalyzeResponse


class ChatService:
    def __init__(self, ai_client: AIClient, session: Session):
        self.ai_client = ai_client
        self.session = session

    async def analyze_and_save(self, user_text: str) -> AnalyzeResponse:
        ai_response = await self.ai_client.analyze_text(user_text)

        db_entry = MessageLog(
            user_message=user_text,
            topic=ai_response.get("topic", "Unknown"),
            language=ai_response.get("language", "Unknown"),
            sentiment=ai_response.get("sentiment", "Unknown"),
            ai_response_text=ai_response.get("text", "No response generated"),
        )

        self.session.add(db_entry)
        self.session.commit()
        self.session.refresh(db_entry)

        return AnalyzeResponse(status="success", response=ai_response.get("text", ""))
