import time
import shutil
import os
from loguru import logger
from app.database.models import SessionLocal, Incident, Event

class DetectionEngine:
    def __init__(self):
        pass 

    def process_event(self, event_type: str, filepath: str):
        db = SessionLocal()
        recent_events = db.query(Event).order_by(Event.id.desc()).limit(30).all()
        
        if len(recent_events) >= 20:
            score = 100 
            
            last_incident = db.query(Incident).order_by(Incident.id.desc()).first()
            if last_incident:
                time_since_last = time.time() - last_incident.timestamp.timestamp()
                if time_since_last < 15:
                    db.close()
                    return 
            
            self.trigger_incident(score, db, recent_events)
            
        db.close()

    def trigger_incident(self, score, db, recent_events):
        logger.critical(f"CRITICAL THREAT DETECTED! Score: {score}")
        print(f"\n🚨 CRITICAL THREAT DETECTED! Score: {score} 🚨\n")
        
        # Phase 5: Quarantine Evidence
        quarantine_dir = "data/quarantine"
        os.makedirs(quarantine_dir, exist_ok=True)
        
        for e in recent_events:
            if os.path.exists(e.file_path) and not e.file_path.endswith('.locked'):
                try:
                    filename = os.path.basename(e.file_path)
                    shutil.copy2(e.file_path, os.path.join(quarantine_dir, filename))
                except Exception:
                    pass 
        logger.info(f"Evidence copied to {quarantine_dir}")
        
        incident = Incident(score=score, level="CRITICAL", details="Mass file encryption burst detected.")
        db.add(incident)
        db.commit()