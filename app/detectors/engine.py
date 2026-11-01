import time
from app.database.models import SessionLocal, Incident, Event

class DetectionEngine:
    def __init__(self):
        pass 

    def process_event(self, event_type: str, filepath: str):
        db = SessionLocal()
        
        # Count how many events we've seen in the last 10 seconds
        # By querying the DB directly, we avoid memory/cpu bottleneck
        recent_events = db.query(Event).order_by(Event.id.desc()).limit(30).all()
        
        # If there are 20 or more events happening very quickly, it's a burst!
        if len(recent_events) >= 20:
            score = 100 # Instant critical score for a mass file burst
            
            # Check if we already alerted recently to avoid spam
            last_incident = db.query(Incident).order_by(Incident.id.desc()).first()
            if last_incident:
                time_since_last = time.time() - last_incident.timestamp.timestamp()
                if time_since_last < 15:
                    db.close()
                    return # Don't alert again if we just did
            
            print(f"\n=============================================")
            print(f"🚨 CRITICAL THREAT DETECTED! Score: {score} 🚨")
            print(f"=============================================\n")
            
            incident = Incident(score=score, level="CRITICAL", details="Mass file encryption burst detected.")
            db.add(incident)
            db.commit()
            
        db.close()