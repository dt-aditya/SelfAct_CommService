import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from celery.result import AsyncResult
from celery_app import celery_app

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


@router.post("/api/v2/sendMessage", response_model=dict)
def queue_message(message: MessageRequest):
    try:
        task = message_service.send_message_task(message)
        return {"task_id": task.id, "status": "Message queued successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.exception("Unexpected error occurred while sending message")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/api/v1/task/{task_id}")
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}
