from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from ..database import get_db
from ..models.job import FileTransferJob
from ..models.alert import AlertLog
from ..schemas.job import JobCreate, JobUpdate, JobResponse
from .auth import get_current_user

router = APIRouter(prefix='/jobs', tags=['jobs'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_jobs(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(FileTransferJob).filter(FileTransferJob.owner_id == user.get('id')).all()

@router.get("/{job_id}", status_code=status.HTTP_200_OK)
async def get_job(user: user_dependency, db: db_dependency, job_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    job = db.query(FileTransferJob).filter(FileTransferJob.id == job_id)\
        .filter(FileTransferJob.owner_id == user.get('id')).first()
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')
    return job

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_job(user: user_dependency, db: db_dependency, job_request: JobCreate):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    job = FileTransferJob(**job_request.model_dump(), owner_id=user.get('id'))
    db.add(job)
    db.commit()

@router.patch("/{job_id}/status", status_code=status.HTTP_200_OK)
async def update_job_status(user: user_dependency, db: db_dependency,
                             job_update: JobUpdate, job_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    job = db.query(FileTransferJob).filter(FileTransferJob.id == job_id)\
        .filter(FileTransferJob.owner_id == user.get('id')).first()
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')
    job.status = job_update.status
    if job_update.retry_count is not None:
        job.retry_count = job_update.retry_count
    if job_update.completed_at is not None:
        job.completed_at = job_update.completed_at
    if job_update.status == 'FAILED':
        alert = AlertLog(
            job_id=job.id,
            alert_type='FAILURE',
            message=f'Job {job.job_name} failed after {job.retry_count} retries.'
        )
        db.add(alert)
    db.add(job)
    db.commit()
    return {"message": "Job status updated successfully"}

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(user: user_dependency, db: db_dependency, job_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    job = db.query(FileTransferJob).filter(FileTransferJob.id == job_id)\
        .filter(FileTransferJob.owner_id == user.get('id')).first()
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')
    db.delete(job)
    db.commit()