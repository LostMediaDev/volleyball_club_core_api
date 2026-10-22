import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker,declarative_base

load_dotenv()

#Local database (for now ig)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./voley.db")

#Config engine
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Global getter for sessionlocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
