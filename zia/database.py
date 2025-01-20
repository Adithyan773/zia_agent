from sqlmodel import SQLModel, Field
from datetime import datetime
from config import settings
from sqlmodel import create_engine

class ChatHistory(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)  # Auto-incrementing primary key
    thread_id: int = Field(nullable=False)
    user_query: str = Field(nullable=False) 
    ai_response: str = Field(nullable=False) 
    timestamp: datetime = Field(default_factory=datetime.utcnow)

engine = create_engine(settings.DEV_DB_URL)

def create_table():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_table()