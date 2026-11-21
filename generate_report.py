import json
import csv
import os
from app.database.models import SessionLocal, Incident, Event

os.makedirs('data', exist_ok=True)
db = SessionLocal()
incidents = db.query(Incident).all()
events = db.query(Event).all()

# JSON
json_data = [{"id": inc.id, "score": inc.score, "level": inc.level, "timestamp": str(inc.timestamp)} for inc in incidents]
with open('data/report.json', 'w') as f:
    json.dump(json_data, f, indent=4)
    
# CSV
with open('data/report.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Event Type', 'File Path', 'Timestamp'])
    for ev in events:
        writer.writerow([ev.id, ev.event_type, ev.file_path, str(ev.timestamp)])

# PDF
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    pdf_file = "data/report.pdf"
    c = canvas.Canvas(pdf_file, pagesize=letter)
    c.drawString(100, 750, "RDRS Incident Report")
    c.drawString(100, 730, f"Total Incidents Detected: {len(incidents)}")
    c.save()
    print("✅ PDF Report saved to data/report.pdf")
except ImportError:
    pass

print("✅ JSON Report saved to data/report.json")
print("✅ CSV Report saved to data/report.csv")
db.close()