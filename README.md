# Ransomware Detection and Response System (RDRS)

## Overview
RDRS is a defensive cybersecurity application that monitors file-system activity in real-time to detect ransomware-like behavior, generate alerts, and support rapid incident response. 

## Architecture
1. **Monitor (`app/detectors/monitor.py`):** Uses `watchdog` to watch a target folder for file creation and modification events.
2. **Detection Engine (`app/detectors/engine.py`):** Analyzes events in a sliding time window. If a massive burst of events occurs (20+ events in 10 seconds), it calculates a Critical threat score (100).
3. **Database (`app/database/models.py`):** Uses SQLite and SQLAlchemy to log events and incident records.
4. **API (`app/api/main.py`):** A FastAPI server that exposes `/status`, `/alerts`, and `/events` endpoints.
5. **Dashboard (`dashboard.html`):** A live web interface that fetches data from the API and displays system status.

## How to Run
1. Create a virtual environment: `python -m venv .venv`
2. Activate it: `.venv\Scripts\activate` (Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Start the API: `python -m uvicorn app.api.main:app --reload`
5. Start the Monitor: `python -c "from app.detectors.monitor import start_monitoring; start_monitoring('data/sandbox')"`
6. Run the simulation: `python run_simulation.py`
7. Open `dashboard.html` in your browser to view the live dashboard.

## Testing
Run `pytest tests/` to execute unit tests for the entropy calculation and engine logic.

## False Positive Mitigation
A potential false positive is a user unzipping a large compressed file (which creates many files quickly). To mitigate this, the engine requires a continuous burst of 20+ file events within a 10-second window, combined with a 15-second alert cooldown, ensuring normal file operations do not trigger critical alerts.