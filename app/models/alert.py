from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class AlertLog(Base):
    __tablename__ = 'alert_logs'

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("file_transfer_jobs.id"))
    alert_type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())