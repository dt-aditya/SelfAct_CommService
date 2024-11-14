# app/services/message_service.py
from sqlalchemy.orm import Session
from app.services.sender import EmailSender, SmsSender, MessageSender
from app.schemas.message_schema import MessageResponse

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
        raise ValueError(f"Unsupported message type: {message_type}")


def send_message(
        db: Session, source: str, recipient: str, msg_content: str, msg_type: MessageType
        ) -> MessageResponse:

    sender = get_message_sender(msg_type)
    status = sender.send(source, recipient, msg_content)

    db_message = Message(
        message_type=msg_type.value,
        source=source,
        recipient=recipient,
        content=msg_content,
        status=status,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
