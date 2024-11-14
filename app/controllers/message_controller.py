import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.services import message_service
from app.schemas.message_schema import MessageRequest, MessageResponse
from app.db.database import get_db

router = APIRouter()


@router.post("/api/v1/sendMessage", response_model=MessageResponse)
def send_message(message: MessageRequest, db: Session = Depends(get_db)):
    try:
        response = message_service.send_message(db=db, message=message)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.exception("Unexpected error occurred while sending message")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")