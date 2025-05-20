from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Load database URL from environment variable
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/test")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
