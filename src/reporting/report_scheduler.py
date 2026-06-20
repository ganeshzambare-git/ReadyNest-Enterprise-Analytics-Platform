"""
automation/report_scheduler.py — Automated Reporting Engine
===========================================================
Simulates an enterprise job scheduler that generates PDFs/CSVs
and emails them to stakeholders.
"""

import time
import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("src.reporting.report_scheduler")
logging.basicConfig(level=logging.INFO)

CONFIG_FILE = Path("automation/schedule_config.json")

class ReportScheduler:
    """Enterprise report scheduling and distribution engine."""

    def __init__(self):
        # Create config file if it doesn't exist
        if not CONFIG_FILE.exists():
            with open(CONFIG_FILE, "w") as f:
                json.dump({"schedules": []}, f)

    def add_schedule(self, report_name: str, frequency: str, format_type: str, emails: str) -> dict:
        """Adds a new automated report to the schedule."""
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
            
            job = {
                "id": str(int(time.time())),
                "name": report_name,
                "frequency": frequency,
                "format": format_type,
                "emails": emails,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "Active"
            }
            data["schedules"].append(job)
            
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=4)
                
            return {"success": True, "job": job}
        except Exception as e:
            logger.error(f"Failed to add schedule: {e}")
            return {"success": False, "error": str(e)}

    def get_schedules(self) -> list:
        """Retrieves all active scheduled reports."""
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                return data.get("schedules", [])
            return []
        except:
            return []

    def trigger_report_now(self, job_id: str) -> dict:
        """Forces an immediate execution of a scheduled report (Simulation)."""
        schedules = self.get_schedules()
        job = next((j for j in schedules if j["id"] == job_id), None)
        
        if not job:
            return {"success": False, "error": "Job not found."}
            
        # Simulate generating the PDF/CSV and sending an email
        logger.info(f"Generating {job['format'].upper()} for {job['name']}...")
        time.sleep(1.5) # Simulate processing time
        
        logger.info(f"Connecting to SMTP Server... Sending to {job['emails']}")
        time.sleep(1.0)
        
        return {
            "success": True,
            "message": f"Successfully generated {job['format'].upper()} report and emailed to {job['emails']}."
        }

    def delete_schedule(self, job_id: str) -> bool:
        """Removes a scheduled job."""
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
            
            data["schedules"] = [j for j in data["schedules"] if j["id"] != job_id]
            
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except:
            return False
