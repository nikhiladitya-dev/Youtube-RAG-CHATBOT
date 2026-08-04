from app.models.conversation_models import (
    ChatMessage,
    Conversation,
)
from datetime import datetime
from pydantic import Field,BaseModel


class ChatMessage(BaseModel):

    role: str
    content: str
    created_at: datetime = Field(
        default_factory=datetime.now
    )


class HistoryService:
    # Stores and manages conversation history.
    def __init__(self):

        self.conversation = Conversation()

    def add_user_message(
        self,
        content: str,
    ) -> None:

        self.conversation.messages.append(

            ChatMessage(
                role="user",
                content=content,
            )

        )

    def add_assistant_message(
        self,
        content: str,
    ) -> None:

        self.conversation.messages.append(

            ChatMessage(
                role="assistant",
                content=content,
            )

        )

    def get_history(
        self,
    ) -> Conversation:

        return self.conversation

    def clear(
        self,
    ) -> None:

        self.conversation = Conversation()