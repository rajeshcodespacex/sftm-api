from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class JobCreate(BaseModel):
    job_name: str
    source_path: str
    destination_path: str
    protocol: str
    file_size_kb: Optional[int] = None
    sla_deadline_minutes: int = 30

class JobUpdate(BaseModel):
    status: str
    retry_count: Optional[int] = None
    completed_at: Optional[datetime] = None

class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_name: str
    source_path: str
    destination_path: str
    protocol: str
    status: str
    file_size_kb: Optional[int]
    retry_count: int
    sla_deadline_minutes: int
    created_at: datetime
    completed_at: Optional[datetime]
    owner_id: int