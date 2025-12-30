import uuid
from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel


class MessageLog(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_message: str
    topic: str
    language: str
    sentiment: str
    ai_response_text: str
