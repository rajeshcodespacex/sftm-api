from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status
from ..database import get_db
from ..models.job import FileTransferJob
from ..models.user import Users
from .auth import get_current_user

router = APIRouter(prefix='/admin', tags=['admin'])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/jobs", status_code=status.HTTP_200_OK)
async def get_all_jobs(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(FileTransferJob).all()

@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).all()

@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(user: user_dependency, db: db_dependency, job_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    job = db.query(FileTransferJob).filter(FileTransferJob.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail='Job not found')
    db.delete(job)
    db.commit()