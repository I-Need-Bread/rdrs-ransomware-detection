import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.detectors.engine import DetectionEngine
from app.database.models import SessionLocal, Event

engine = DetectionEngine()

class RansomwareHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            self.log_event("MODIFIED", event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.log_event("CREATED", event.src_path)

    def log_event(self, event_type, path):
        path = path.replace('\\\\', '\\')
        
        db = SessionLocal()
        new_event = Event(event_type=event_type, file_path=path)
        db.add(new_event)
        db.commit()
        db.close()
        
        # Send to engine
        engine.process_event(event_type, path)

def start_monitoring(watch_path: str):
    absolute_path = os.path.abspath(watch_path)
    
    event_handler = RansomwareHandler()
    observer = Observer()
    observer.schedule(event_handler, absolute_path, recursive=True)
    observer.start()
    print(f"🛡️ Monitoring started on {absolute_path}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()