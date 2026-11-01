from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    event_type = Column(String)
    file_path = Column(String)
    entropy = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Incident(Base):
    __tablename__ = 'incidents'
    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    level = Column(String)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)
engine = create_engine('sqlite:///data/rdrs.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)