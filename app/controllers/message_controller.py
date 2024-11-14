from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services import message_service
from app.schemas.message_schema import MessageRequest, MessageResponse
from app.db.database import SessionLocal

router = APIRouter()


# TODO: Convert to connection pool
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/api/v1/sendMessage", response_model=MessageResponse)
def send_message(message: MessageRequest, db: Session = Depends(get_db)):
    return message_service.send_message(db, message.source, message.recipient, message.content, message.message_type)