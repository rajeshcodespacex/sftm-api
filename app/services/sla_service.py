from sqlalchemy.orm import Session
from ..models.job import FileTransferJob
from ..models.alert import AlertLog
from datetime import datetime, timezone

def check_sla_breaches(db: Session, user_id: int):
    jobs = db.query(FileTransferJob).filter(
        FileTransferJob.owner_id == user_id,
        FileTransferJob.status == 'RUNNING'
    ).all()

    breached = []
    for job in jobs:
        if job.created_at:
            now = datetime.now(timezone.utc)
            elapsed_minutes = (now - job.created_at).total_seconds() / 60
            if elapsed_minutes > job.sla_deadline_minutes:
                existing_alert = db.query(AlertLog).filter(
                    AlertLog.job_id == job.id,
                    AlertLog.alert_type == 'SLA_BREACH'
                ).first()
                if not existing_alert:
                    alert = AlertLog(
                        job_id=job.id,
                        alert_type='SLA_BREACH',
                        message=f'Job "{job.job_name}" breached SLA of {job.sla_deadline_minutes} minutes.'
                    )
                    db.add(alert)
                    breached.append(job.job_name)
    db.commit()
    return breached