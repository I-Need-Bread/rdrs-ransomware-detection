from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.database.models import SessionLocal, Incident, Event
import uvicorn

app = FastAPI(title="RDRS API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def get_status():
    return {"status": "active", "message": "RDRS is monitoring"}

@app.get("/alerts")
def get_alerts():
    db = SessionLocal()
    alerts = db.query(Incident).all()
    db.close()
    return alerts

@app.get("/events")
def get_events():
    db = SessionLocal()
    events = db.query(Event).order_by(Event.id.desc()).limit(20).all()
    db.close()
    return events