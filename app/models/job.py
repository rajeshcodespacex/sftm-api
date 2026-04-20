from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class FileTransferJob(Base):
    __tablename__ = 'file_transfer_jobs'

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, nullable=False)
    source_path = Column(String, nullable=False)
    destination_path = Column(String, nullable=False)
    protocol = Column(String, nullable=False)  # SFTP, FTPS, HTTPS
    status = Column(String, default='PENDING')  # PENDING, RUNNING, SUCCESS, FAILED
    file_size_kb = Column(Integer, nullable=True)
    retry_count = Column(Integer, default=0)
    sla_deadline_minutes = Column(Integer, default=30)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))