from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from ..database import get_db
from ..models.alert import AlertLog
from ..models.job import FileTransferJob
from .auth import get_current_user
from ..services.sla_service import check_sla_breaches

router = APIRouter(prefix='/alerts', tags=['alerts'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_alerts(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_job_ids = db.query(FileTransferJob.id)\
        .filter(FileTransferJob.owner_id == user.get('id')).all()
    job_ids = [j[0] for j in user_job_ids]
    return db.query(AlertLog).filter(AlertLog.job_id.in_(job_ids)).all()

@router.post("/check-sla", status_code=status.HTTP_200_OK)
async def trigger_sla_check(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    breached_jobs = check_sla_breaches(db, user.get('id'))
    if not breached_jobs:
        return {"message": "No SLA breaches found", "breached_jobs": []}
    return {
        "message": f"{len(breached_jobs)} SLA breach(es) detected",
        "breached_jobs": breached_jobs
    }