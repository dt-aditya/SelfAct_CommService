import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.main import app
from app.db.database import Base, get_db
from app.services.message_service import get_message_sender
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

mock_sender = MagicMock()
def override_get_message_sender():
    return mock_sender

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_message_sender] = override_get_message_sender

client = TestClient(app)

@pytest.fixture
def mock_send_message():
    mock_sender.send.return_value = "SENT"  # Mock the sender's response status

def test_send_message_success(mock_send_message):
    payload = {
        "message_type": "email",
        "source": "test@example.com",
        "recipient": "recipient@example.com",
        "content": "Hello, this is a test message!"
    }

    response = client.post("/api/v1/sendMessage", json=payload)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "Success"
    assert response_data["recipient"] == payload["recipient"]

def test_send_message_invalid_type():
    payload = {
        "message_type": "INVALID_TYPE",
        "source": "test@example.com",
        "recipient": "recipient@example.com",
        "content": "This should fail"
    }

    response = client.post("/api/v1/sendMessage", json=payload)

    assert response.status_code == 422
    response_detail = response.json()["detail"][0]
    assert response_detail["type"] == "enum"
    assert response_detail["msg"] == "Input should be 'email' or 'sms'"
    assert response_detail["input"] == "INVALID_TYPE"
