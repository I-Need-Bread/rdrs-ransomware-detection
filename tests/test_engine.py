from app.detectors.engine import DetectionEngine
from app.database.models import SessionLocal, Incident, Event

def test_critical_burst():
    db = SessionLocal()
    db.query(Incident).delete() 
    db.query(Event).delete() 
    db.commit()
    
    engine = DetectionEngine()
    
    # We must add 25 events to the database first so the engine can count them
    for i in range(25):
        new_event = Event(event_type="MODIFIED", file_path=f"fake_file_{i}.txt")
        db.add(new_event)
    db.commit()
    
    # Now trigger the engine
    engine.process_event("MODIFIED", "fake_file_final.txt")
        
    incidents = db.query(Incident).all()
    assert len(incidents) > 0
    db.close()