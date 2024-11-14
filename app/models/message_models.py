from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import func
from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_type = Column(String, index=True)
    source = Column(String)
    recipient = Column(String)
    content = Column(String)
    status = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

