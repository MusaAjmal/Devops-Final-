from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()



DATABASE_URL ="postgresql://avnadmin:AVNS_OQ0K1gICnzak5iV_ukC@pg-35318557-cuilahore-63ed.j.aivencloud.com:19969/defaultdb?sslmode=require"
# if not DATABASE_URL:
#     raise ValueError("No DATABASE_URL set in environment variables")

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Session = sessionmaker()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()