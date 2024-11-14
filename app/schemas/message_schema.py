from pydantic import BaseModel
from datetime import datetime
from app.core.message_type import MessageType


class MessageRequest(BaseModel):
    message_type: MessageType
    source: str
    recipient: str
    content: str
    

class MessageResponse(BaseModel):
    id: int
    message_type: str
    recipient: str
    content: str
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True