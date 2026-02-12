from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from db import get_db
from repositories.chat_repo import ChatRepo
from schemas.chat_schemas import (
    ChatSessionCreate,
    ChatSessionUpdate,
    ChatSessionResponse,
)
from typing import List

router = APIRouter(prefix="/chat", tags=["Chat History"])


@router.get("/sessions", response_model=List[ChatSessionResponse])
def get_sessions(email: str = Query(..., description="User email"), db: Session = Depends(get_db)):
    """Get all chat sessions for a user."""
    chat_repo = ChatRepo(db)
    sessions = chat_repo.get_sessions_by_email(email)
    return sessions


@router.post("/sessions", response_model=ChatSessionResponse)
def create_session(data: ChatSessionCreate, db: Session = Depends(get_db)):
    """Save a new chat session."""
    chat_repo = ChatRepo(db)
    session = chat_repo.create_session(
        user_email=data.user_email,
        title=data.title,
        pinned=data.pinned,
        folder=data.folder,
        messages=data.messages,
    )
    return session


@router.put("/sessions/{session_id}", response_model=ChatSessionResponse)
def update_session(session_id: int, data: ChatSessionUpdate, db: Session = Depends(get_db)):
    """Update a chat session (rename, pin, move folder)."""
    chat_repo = ChatRepo(db)
    session = chat_repo.update_session(
        session_id,
        title=data.title,
        pinned=data.pinned,
        folder=data.folder,
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    """Delete a chat session."""
    chat_repo = ChatRepo(db)
    success = chat_repo.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}
