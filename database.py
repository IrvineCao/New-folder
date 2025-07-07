import json
import singlestoredb as s2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

# Function to load database configuration from config.json
def load_config():
    with open('config.json') as f:
        return json.load(f)

# Load configuration
config = load_config()

# Construct the database URL for SQLAlchemy
# Format: dialect+driver://username:password@host:port/database
SQLALCHEMY_DATABASE_URL = (
    f"singlestoredb://{config['db_user']}:{config['db_password']}@"
    f"{config['db_host']}:{config['db_port']}/{config['db_name']}"
)

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_connection():
    """Context manager for providing a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()