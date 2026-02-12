from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatMessageSchema(BaseModel):
    role: str
    content: str


class ChatSessionCreate(BaseModel):
    user_email: str
    title: str = "New Chat"
    messages: List[ChatMessageSchema] = []
    pinned: bool = False
    folder: str = "default"


class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None
    pinned: Optional[bool] = None
    folder: Optional[str] = None


class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    id: int
    user_email: str
    title: str
    pinned: bool
    folder: str
    created_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True
