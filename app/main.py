from fastapi import FastAPI
from app.db import database
from app.controllers import message_controller

# Initialize the database (if not already done)
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Include the router from the message controller
app.include_router(message_controller.router)