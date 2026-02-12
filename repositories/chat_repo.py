from sqlalchemy.orm import Session
from models import ChatSession, ChatMessage


class ChatRepo:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_email: str, title: str, pinned: bool = False, folder: str = "default", messages: list = []):
        session = ChatSession(
            user_email=user_email,
            title=title,
            pinned=pinned,
            folder=folder,
        )
        self.db.add(session)
        self.db.flush()  # get the session.id

        for msg in messages:
            message = ChatMessage(
                session_id=session.id,
                role=msg.role,
                content=msg.content,
            )
            self.db.add(message)

        self.db.commit()
        self.db.refresh(session)
        return session

    def get_sessions_by_email(self, user_email: str):
        return (
            self.db.query(ChatSession)
            .filter(ChatSession.user_email == user_email)
            .order_by(ChatSession.created_at.desc())
            .all()
        )

    def get_session_by_id(self, session_id: int):
        return self.db.query(ChatSession).filter(ChatSession.id == session_id).first()

    def update_session(self, session_id: int, **kwargs):
        session = self.get_session_by_id(session_id)
        if not session:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(session, key):
                setattr(session, key, value)
        self.db.commit()
        self.db.refresh(session)
        return session

    def delete_session(self, session_id: int):
        session = self.get_session_by_id(session_id)
        if not session:
            return False
        self.db.delete(session)
        self.db.commit()
        return True
