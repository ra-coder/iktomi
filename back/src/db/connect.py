from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Database URL (replace with your DB config)


# Sync SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL)

# Base class for ORM models
Base = declarative_base()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
