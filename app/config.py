import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    USE_QUEUE = os.getenv("USE_QUEUE", False)
    USE_LOG_BUFFER = os.getenv("USE_LOG_BUFFER", False)

config = Config()