from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    alert_type: str
    message: str
    created_at: datetime