from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# from dotenv import load_dotenv
# import os

# load_dotenv()
# # DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("No DATABASE_URL set in environment variables")

engine = create_engine(
   
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Session = sessionmaker()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()