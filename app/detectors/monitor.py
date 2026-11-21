import time
import os
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from loguru import logger
from app.detectors.engine import DetectionEngine
from app.database.models import SessionLocal, Event

# Setup Logging
os.makedirs("data/logs", exist_ok=True)
logger.add("data/logs/rdrs.log", rotation="10 MB", level="INFO")

engine = DetectionEngine()

# Phase 3: Process Metadata
def get_suspect_process():
    suspects = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] > 0:
                suspects.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if suspects:
        suspects = sorted(suspects, key=lambda x: x['cpu_percent'], reverse=True)
        return suspects[0]['name']
    return "Unknown"

class RansomwareHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            self.log_event("MODIFIED", event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.log_event("CREATED", event.src_path)

    def log_event(self, event_type, path):
        path = path.replace('\\\\', '\\')
        suspect = get_suspect_process()
        logger.info(f"{event_type} -> {path} | Suspect Process: {suspect}")
        
        db = SessionLocal()
        new_event = Event(event_type=event_type, file_path=path)
        db.add(new_event)
        db.commit()
        db.close()
        
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