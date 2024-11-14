import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.sender import EmailSender, SmsSender, MessageSender
from app.schemas.message_schema import MessageResponse, MessageRequest
from app.core import MessageType, MessageStatus
from app.models.message_models import Message


def get_message_sender(message_type: MessageType) -> MessageSender:
    """
    Return the correct message sender based on the mentioned type.
    """
    if message_type == MessageType.EMAIL:
        return EmailSender()
    elif message_type == MessageType.SMS:
        return SmsSender()
    else:
        logging.error(f"Unsupported message type: {message_type}")
        raise HTTPException(status_code=400, detail="Unsupported message type.")


def send_message(db: Session, message: MessageRequest) -> MessageResponse:
    sender = get_message_sender(message.message_type)
    status = sender.send(message.source, message.recipient, message.content)

    db_message = Message(
        message_type=message.message_type.value,
        source=message.source,
        recipient=message.recipient,
        content=message.content,
        status=status,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return MessageResponse(
        id=db_message.id,
        message_type=db_message.message_type,
        recipient=db_message.recipient,
        content=db_message.content,
        status=db_message.status,
        timestamp=db_message.timestamp
    )