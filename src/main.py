from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import SessionLocal, Prospect, EmailCampaign, Meeting
from prospect_researcher import ProspectResearcher
from email_generator import EmailGenerator
from meeting_scheduler import MeetingScheduler
from knowledge_base import KnowledgeBase
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

app = FastAPI(title="AI SDR - Sales Development Representative", version="1.0.0")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize AI components
prospect_researcher = ProspectResearcher()
email_generator = EmailGenerator()
meeting_scheduler = MeetingScheduler()
knowledge_base = KnowledgeBase()

# Pydantic models
class ProspectCreate(BaseModel):
    name: str
    email: str
    company: str
    title: Optional[str] = None

class EmailRequest(BaseModel):
    prospect_id: int
    email_type: str = "initial"

@app.get("/")
def read_root():
    return {"message": "AI SDR - Sales Development Representative API"}

@app.post("/prospects/", response_model=dict)
def create_prospect(prospect: ProspectCreate, db: Session = Depends(get_db)):
    # Research the prospect
    research_data = prospect_researcher.research_prospect(
        prospect.name, 
        prospect.company, 
        prospect.email
    )
    
    # Create prospect in database
    db_prospect = Prospect(
        name=prospect.name,
        email=prospect.email,
        company=prospect.company,
        title=research_data.get("title"),
        industry=research_data.get("industry"),
        company_size=research_data.get("company_size"),
        linkedin_url=research_data.get("linkedin_url"),
        pain_points=str(research_data.get("pain_points"))
    )
    
    db.add(db_prospect)
    db.commit()
    db.refresh(db_prospect)
    
    return {"prospect_id": db_prospect.id, "research_data": research_data}

@app.get("/prospects/", response_model=List[dict])
def get_prospects(db: Session = Depends(get_db)):
    prospects = db.query(Prospect).all()
    return [{"id": p.id, "name": p.name, "company": p.company, "status": p.status} for p in prospects]

@app.post("/email/generate/")
def generate_email(request: EmailRequest, db: Session = Depends(get_db)):
    # Get prospect data
    prospect = db.query(Prospect).filter(Prospect.id == request.prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")
    
    prospect_data = {
        "name": prospect.name,
        "company": prospect.company,
        "title": prospect.title,
        "industry": prospect.industry,
        "pain_points": prospect.pain_points
    }
    
    # Generate email
    if request.email_type == "initial":
        email_data = email_generator.generate_initial_email(prospect_data)
    else:
        follow_up_num = int(request.email_type.split("_")[-1]) if "_" in request.email_type else 1
        email_data = email_generator.generate_follow_up(prospect_data, follow_up_num)
    
    # Save to database
    email_campaign = EmailCampaign(
        prospect_id=request.prospect_id,
        subject=email_data["subject"],
        content=email_data["content"],
        email_type=request.email_type,
        sent_at=datetime.utcnow()
    )
    
    db.add(email_campaign)
    db.commit()
    
    return email_data

@app.post("/meeting/schedule/")
def schedule_meeting(prospect_id: int, db: Session = Depends(get_db)):
    prospect = db.query(Prospect).filter(Prospect.id == prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect not found")
    
    prospect_data = {
        "name": prospect.name,
        "company": prospect.company
    }
    
    meeting_email = meeting_scheduler.generate_scheduling_email(prospect_data)
    available_times = meeting_scheduler.propose_meeting_times()
    
    return {
        "email": meeting_email,
        "available_times": [t.isoformat() for t in available_times]
    }

@app.get("/analytics/")
def get_analytics(db: Session = Depends(get_db)):
    total_prospects = db.query(Prospect).count()
    total_emails = db.query(EmailCampaign).count()
    total_meetings = db.query(Meeting).count()
    
    # Calculate engagement metrics
    replied_emails = db.query(EmailCampaign).filter(EmailCampaign.replied == True).count()
    engagement_rate = (replied_emails / total_emails * 100) if total_emails > 0 else 0
    
    return {
        "total_prospects": total_prospects,
        "total_emails": total_emails,
        "total_meetings": total_meetings,
        "engagement_rate": round(engagement_rate, 2)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

