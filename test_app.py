import pytest
from app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.secret_key = "test_secret_key"  # Required for session/flash
    with app.test_client() as client:
        yield client

# ---------- Test: Submit Feedback (Valid) ----------
@patch("app.cursor")
def test_submit_feedback(mock_cursor, client):
    data = {"name": "Alice", "message": "This is a test message."}
    response = client.post("/", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Thank you for your feedback" in response.data

# ---------- Test: Submit Feedback (No Message) ----------
def test_submit_feedback_without_message(client):
    data = {"name": "Bob", "message": ""}
    response = client.post("/", data=data, follow_redirects=True)
    assert response.status_code == 200


# ---------- Test: View Feedback ----------
@patch("app.cursor")
def test_view_feedback(mock_cursor, client):
    mock_cursor.fetchall.return_value = [
        (1, "Alice", "Great job!", False),
        (2, None, "Anonymous message", True)
    ]
    response = client.get("/feedback")
    assert response.status_code == 200
    assert b"Great job!" in response.data
    assert b"Anonymous message" in response.data

# ---------- Test: Export Feedback ----------
@patch("app.cursor")
def test_export_feedback(mock_cursor, client):
    mock_cursor.fetchall.return_value = [
        (1, "Alice", "Nice!", False),
        (2, None, "Thanks!", True)
    ]
    response = client.get("/export")
    assert response.status_code == 200
    assert response.mimetype == "text/csv"
    assert b"Alice" in response.data
    assert b"Thanks!" in response.data
