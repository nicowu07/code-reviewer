from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
import dotenv
from pathlib import Path

Base = declarative_base()

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
dotenv.load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
data_engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=data_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

