from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


# Local database (for now ig)
SQLALCHEMY_DATABASE_URL = "sqlite///./voley_academy.db"

# Config engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False}
)


Sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base

# global getter for sessionlocal
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
