from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Define the SQLite Database URL
# This creates a file named 'sql_app.db' in your project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 2. Create the Engine
# 'check_same_thread' is only needed for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class
# Each instance of this will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create the Base class
# Our models in models.py will inherit from this
Base = declarative_base()

# 5. Dependency to get the DB session
# This ensures the connection is closed after a request is finished
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()