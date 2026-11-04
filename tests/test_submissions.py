import pytest

from fastapi.testclient import TestClient

from app import database
from app.main import app


# --------------------------------------------------
# TEST DATABASE CONFIGURATION
# --------------------------------------------------

@pytest.fixture
def client(tmp_path, monkeypatch):
    """
    Creates an isolated temporary SQLite database
    for each test execution.
    """

    test_database = tmp_path / "test_submissions.db"

    monkeypatch.setattr(
        database,
        "get_database_path",
        lambda: str(test_database)
    )

    with TestClient(app) as test_client:
        yield test_client


# --------------------------------------------------
# SAMPLE VALID SUBMISSION
# --------------------------------------------------

VALID_SUBMISSION = {
    "student_name": "Ali Ahmed",
    "registration_number": "FA24-BCS-001",
    "assignment_title": "DevOps Laboratory Midterm",
    "submission_url": "https://github.com/Zainab-zaini"
}


# --------------------------------------------------
# TEST 1: VALID ASSIGNMENT SUBMISSION
# --------------------------------------------------

def test_valid_submission_is_saved_and_displayed(client):

    response = client.post(
        "/api/submissions",
        json=VALID_SUBMISSION
    )

    assert response.status_code == 201

    saved_submission = response.json()

    assert saved_submission["student_name"] == "Ali Ahmed"

    assert saved_submission["registration_number"] == "FA24-BCS-001"

    assert saved_submission["assignment_title"] == (
        "DevOps Laboratory Midterm"
    )

    assert saved_submission["submission_url"] == (
        "https://github.com/Zainab-zaini"
    )

    assert saved_submission["id"] is not None

    # Verify that the submission appears in the list.

    list_response = client.get("/api/submissions")

    assert list_response.status_code == 200

    result = list_response.json()

    assert result["total"] == 1

    assert len(result["submissions"]) == 1

    assert (
        result["submissions"][0]["registration_number"]
        == "FA24-BCS-001"
    )


# --------------------------------------------------
# TEST 2: MISSING REGISTRATION NUMBER
# --------------------------------------------------

def test_missing_registration_number_is_rejected(client):

    invalid_submission = VALID_SUBMISSION.copy()

    invalid_submission["registration_number"] = ""

    response = client.post(
        "/api/submissions",
        json=invalid_submission
    )

    assert response.status_code == 422

    # Validation failure must not save any record.

    list_response = client.get("/api/submissions")

    assert list_response.status_code == 200

    assert list_response.json()["total"] == 0

    assert list_response.json()["submissions"] == []


# --------------------------------------------------
# TEST 3: INVALID SUBMISSION URL
# --------------------------------------------------

def test_invalid_submission_url_is_rejected(client):

    invalid_submission = VALID_SUBMISSION.copy()

    invalid_submission["submission_url"] = (
        "not-a-valid-url.example"
    )

    response = client.post(
        "/api/submissions",
        json=invalid_submission
    )

    assert response.status_code == 422

    # Invalid URLs must never enter the database.

    list_response = client.get("/api/submissions")

    assert list_response.status_code == 200

    assert list_response.json()["total"] == 0

    assert list_response.json()["submissions"] == []


# --------------------------------------------------
# ADDITIONAL TEST 4: HEALTH CHECK
# --------------------------------------------------

def test_application_health_check(client):

    response = client.get("/api/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


# --------------------------------------------------
# ADDITIONAL TEST 5: EMPTY SUBMISSION LIST
# --------------------------------------------------

def test_empty_submission_list(client):

    response = client.get("/api/submissions")

    assert response.status_code == 200

    assert response.json()["total"] == 0

    assert response.json()["submissions"] == []