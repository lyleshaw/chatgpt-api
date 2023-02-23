from typing import Optional

from pydantic import BaseModel


class ChatMessage:
    Id: str
    Text: str
    Role: str
    ParentMessageId: str
    ConversationId: str
    Detail: Optional[any]


class ChatContext(BaseModel):
    conversationId: Optional[str]
    parentMessageId: Optional[str]


class ChatRequest(BaseModel):
    prompt: str
    options: Optional[ChatContext]


class ChatResponse(BaseModel):
    role: str = "assistant"
    id: Optional[str] = None
    parentMessageId: Optional[str] = None
    conversationId: Optional[str] = None
    text: str
