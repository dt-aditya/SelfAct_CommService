from fastapi import FastAPI
from app.db import database
from app.controllers import message_controller

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(message_controller.router)