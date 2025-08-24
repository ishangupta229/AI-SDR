from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Prospect(Base):
    __tablename__ = "prospects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    company = Column(String)
    title = Column(String)
    linkedin_url = Column(String)
    phone = Column(String)
    industry = Column(String)
    company_size = Column(String)
    pain_points = Column(Text)
    engagement_score = Column(Float, default=0.0)
    status = Column(String, default="new")  # new, contacted, replied, meeting_scheduled, converted
    created_at = Column(DateTime, default=datetime.utcnow)

class EmailCampaign(Base):
    __tablename__ = "email_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    prospect_id = Column(Integer, index=True)
    subject = Column(String)
    content = Column(Text)
    email_type = Column(String)  # initial, follow_up_1, follow_up_2, etc.
    sent_at = Column(DateTime)
    opened = Column(Boolean, default=False)
    clicked = Column(Boolean, default=False)
    replied = Column(Boolean, default=False)

class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    prospect_id = Column(Integer, index=True)
    scheduled_time = Column(DateTime)
    meeting_link = Column(String)
    transcript = Column(Text)
    action_items = Column(Text)
    outcome = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)
