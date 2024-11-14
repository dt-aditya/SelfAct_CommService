from celery import shared_task
from app.db.database import SessionLocal
from app.models.message_models import Message
from app.db.redis import redis_client
import json

@shared_task
def flush_log_buffer_task():
    db = SessionLocal()
    try:
        # Retrieve all log messages from Redis
        logs_to_flush = []
        while True:
            log = redis_client.lpop("log_buffer")
            if log is None:
                break  # No more logs to flush
            logs_to_flush.append(json.loads(log))
        
        if logs_to_flush:
            print("Flushing buffer now")
            # Perform bulk insert
            db.execute(
                Message.__table__.insert(),
                logs_to_flush
            )
            db.commit()
    finally:
        db.close()
