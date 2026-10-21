from database import Base
from sqlalchemy import Text,String,Column,Integer,DateTime
from sqlalchemy.sql import func

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer , primary_key=True)
    title = Column(Text , nullable=False)
    url = Column(Text , nullable=False , unique=True)
    source = Column(String , nullable=True)           # nullable is also True By Default
    score = Column(Integer , nullable=True)
    summary = Column(Text , nullable=True)
    discovered_at = Column(DateTime , server_default=func.now())
