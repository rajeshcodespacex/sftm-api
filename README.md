# Secure File Transfer Management API

A production-grade REST API built with FastAPI and PostgreSQL to monitor and manage secure file transfer jobs, track SLA compliance, and generate alerts.

## Tech Stack

- **FastAPI** — Python web framework
- **PostgreSQL** — Relational database
- **SQLAlchemy** — ORM
- **JWT Authentication** — Secure token-based auth
- **Passlib + Bcrypt** — Password hashing
- **Alembic** — Database migrations
- **Uvicorn** — ASGI server

## Features

- JWT-based user authentication (register, login)
- Create and manage file transfer jobs (SFTP, FTPS, HTTPS)
- Track job status — PENDING, RUNNING, SUCCESS, FAILED
- SLA breach detection and alert generation
- Dashboard summary — total jobs, success rate, failed count, SLA breaches
- Role-based access control (admin vs regular user)
- Admin panel — view all users and jobs

## Project Structure

SFTM-API/
app/
models/       — SQLAlchemy database models
schemas/      — Pydantic request/response models
routers/      — API route handlers
services/     — Business logic (SLA checking)
auth/         — JWT authentication
main.py       — FastAPI app entry point
database.py   — Database connection
.env            — Environment variables