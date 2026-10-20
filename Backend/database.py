import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

load_dotenv()

db_username = os.getenv("username")
db_pswd = os.getenv("password")
db_port = os.getenv("port")
db_host = os.getenv("host")
db_name = os.getenv("database_name")

Database_URL = f"postgresql://{db_username}:{db_pswd}@{db_host}:{db_port}/{db_name}"
engine = create_engine(Database_URL)

SessionLocal = sessionmaker(bind=engine)
base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    


