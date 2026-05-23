from datetime import datetime

from pydantic import BaseModel, Field

from history.constants import MESSAGE_ROLE_USER


class MessageInput(BaseModel):
    role: str = Field(default=MESSAGE_ROLE_USER)
    content: str = Field(min_length=1)


class StartConversationRequest(BaseModel):
    user_id: str | None = None
    title: str | None = None
    initial_message: MessageInput


class StartConversationResponse(BaseModel):
    conversation_id: str
    message_id: str
    created_at: datetime
    updated_at: datetime


class AppendMessageRequest(BaseModel):
    role: str = Field(default=MESSAGE_ROLE_USER)
    content: str = Field(min_length=1)


class AppendMessageResponse(BaseModel):
    conversation_id: str
    message_id: str
    updated_at: datetime


class DeleteConversationResponse(BaseModel):
    conversation_id: str
    deleted: bool
