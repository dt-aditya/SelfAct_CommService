from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def env_setup():
    os.environ["DATABASE_URL"] = DATABASE_URL

def get_test_engine():
    return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
