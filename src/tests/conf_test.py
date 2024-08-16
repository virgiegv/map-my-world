import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from src.db import models
from sqlalchemy.sql import text

@pytest.fixture(scope='function')
def db_session():
    # Set up the database engine and session
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/testmapmyworld"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    models.Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    # Provide the session to the test
    yield session

    # Teardown code: drop all tables
    session.rollback()
    session.close()
    models.Base.metadata.drop_all(bind=engine)