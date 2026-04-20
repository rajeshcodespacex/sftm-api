from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, jobs, admin, users, alerts

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Secure File Transfer Management API",
    description="Monitor and manage secure file transfer jobs, SLA tracking and alerts",
    version="1.0.0"
)

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(alerts.router)