from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (replace with your DB config)
DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

# Sync SQLAlchemy engine
engine = create_engine(DATABASE_URL)

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
