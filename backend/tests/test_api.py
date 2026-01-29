"""
Unit tests for CV Analysis API
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import io


client = TestClient(app)


def test_root_endpoint():
    """Test root health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_health_endpoint():
    """Test detailed health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "checks" in data


def test_analyze_endpoint_missing_file():
    """Test analyze endpoint without file"""
    response = client.post(
        "/api/analyze",
        data={"job_description": "Looking for a Python developer with FastAPI experience"}
    )
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_missing_job_description():
    """Test analyze endpoint without job description"""
    # Create a fake PDF file
    fake_pdf = io.BytesIO(b"fake pdf content")
    
    response = client.post(
        "/api/analyze",
        files={"cv_file": ("test.pdf", fake_pdf, "application/pdf")}
    )
    assert response.status_code == 422  # Validation error


def test_analyze_endpoint_invalid_file_type():
    """Test analyze endpoint with non-PDF file"""
    fake_file = io.BytesIO(b"not a pdf")
    
    response = client.post(
        "/api/analyze",
        files={"cv_file": ("test.txt", fake_file, "text/plain")},
        data={"job_description": "Looking for a Python developer"}
    )
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_analyze_endpoint_short_job_description():
    """Test analyze endpoint with too short job description"""
    fake_pdf = io.BytesIO(b"%PDF-1.4 fake pdf")
    
    response = client.post(
        "/api/analyze",
        files={"cv_file": ("test.pdf", fake_pdf, "application/pdf")},
        data={"job_description": "short"}
    )
    assert response.status_code == 400


# Note: Full integration test with real PDF would require a valid PDF file
# and would be better suited for integration tests
