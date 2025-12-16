import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import Base, get_db  # adjust path if needed


# Create SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- FIXTURES --- #

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables before tests, drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope="function")
def db_session():
    """Provide a new database session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Create a TestClient with a test DB session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c
