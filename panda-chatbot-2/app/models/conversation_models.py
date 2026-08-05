from pydantic import BaseModel, Field
class ChatMessage(BaseModel):
    role: str = Field(
        description="user or assistant"
    )

    content: str

class Conversation(BaseModel):
    messages: list[ChatMessage] = Field(default_factory=list)