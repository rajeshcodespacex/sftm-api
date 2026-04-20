from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/healthy")
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy"}

def test_register_user():
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "testuser@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test123",
        "role": "user",
        "phone_number": "9999999999"
    })
    response = client.post("/auth/register", json={
        "username": "testuser_new",
        "email": "testuser_new@gmail.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "test123",
        "role": "user",
        "phone_number": "9999999990"
    })
    assert response.status_code == 201

def test_register_duplicate_user():
    client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dupuser@gmail.com",
        "first_name": "Dup",
        "last_name": "User",
        "password": "test123",
        "role": "user",
        "phone_number": "7777777777"
    })
    response = client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dupuser@gmail.com",
        "first_name": "Dup",
        "last_name": "User",
        "password": "test123",
        "role": "user",
        "phone_number": "7777777777"
    })
    assert response.status_code == 400

def test_login_user():
    client.post("/auth/register", json={
        "username": "logintest",
        "email": "logintest@gmail.com",
        "first_name": "Login",
        "last_name": "Test",
        "password": "test123",
        "role": "user",
        "phone_number": "8888888888"
    })
    response = client.post("/auth/token", data={
        "username": "logintest",
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    response = client.post("/auth/token", data={
        "username": "logintest",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_jobs_without_auth():
    response = client.get("/jobs/")
    assert response.status_code == 401

def test_create_job_without_auth():
    response = client.post("/jobs/", json={
        "job_name": "Test Job",
        "source_path": "/source/test.csv",
        "destination_path": "/dest/test.csv",
        "protocol": "SFTP",
        "file_size_kb": 1024,
        "sla_deadline_minutes": 30
    })
    assert response.status_code == 401

def test_get_alerts_without_auth():
    response = client.get("/alerts/")
    assert response.status_code == 401