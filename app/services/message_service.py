import logging
import json
from celery import shared_task
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.sender import EmailSender, SmsSender, MessageSender
from app.schemas.message_schema import MessageResponse, MessageRequest
from app.core import MessageType, MessageStatus
from app.models.message_models import Message
from app.db.database import SessionLocal
from app.db.redis import redis_client
from app.tasks.log_buffer import add_log_to_buffer
from app.config import config

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


def send_message(db: Session, message: MessageRequest):
    try:
        sender = get_message_sender(message.message_type)
        status = sender.send(message.source, message.recipient, message.content)
        write_message_to_db(db, message, status)
        return {"detail": "Message Sent"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=f"{e}")


@shared_task
def send_message_task(message: dict):
    db = SessionLocal()
    try:
        message = MessageRequest.model_validate(message)
        sender = get_message_sender(message.message_type)
        status = sender.send(message.source, message.recipient, message.content)
        write_message_to_db(db, message, status)
        return {"detail": "Message Queued"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=f"{e}")


def write_message_to_db(
        db: Session, message: dict, status: MessageStatus):
    if config.USE_LOG_BUFFER:
        log_message(message)
    else:
        try:
            db_message = Message(
                message_type=message.message_type,
                source=message.source,
                recipient=message.recipient,
                content=message.content,
                status=status.value,
            )
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
        finally:
            db.close()


def log_message(message: Message):
    message_data = {
        "message_type": message.message_type,
        "source": message.source,
        "recipient": message.recipient,
        "content": message.content,
        "status": "QUEUED",
    }
    redis_client.rpush("log_buffer", json.dumps(message_data))

