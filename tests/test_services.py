import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models.message_models import Message
from fastapi.testclient import TestClient
from app.main import app


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Override the dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[override_get_db] = override_get_db

def test_create_message():
    with TestingSessionLocal() as db:
        # Create a new Message object
        new_message = Message(
            message_type="text",
            source="user_1",
            recipient="user_2",
            content="Hello!",
            status="sent"
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        
        assert new_message.id is not None
        assert new_message.message_type == "text"
        assert new_message.source == "user_1"
        assert new_message.recipient == "user_2"
        assert new_message.content == "Hello!"
        assert new_message.status == "sent"