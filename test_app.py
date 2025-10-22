import pytest
from app import app, get_db_connection

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            # Re-initialize SQLite in-memory DB for each test session
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS feedback")
            cursor.execute("""
                CREATE TABLE feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    message TEXT,
                    is_read BOOLEAN DEFAULT 0
                )
            """)
            conn.commit()
        yield client


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200


def test_submit_feedback(client):
    response = client.post('/', data={
        'name': 'Alice',
        'message': 'Great class!'
    }, follow_redirects=True)

    assert response.status_code == 200


def test_submit_feedback_without_message(client):
    response = client.post('/', data={
        'name': 'Bob',
        'message': ''
    }, follow_redirects=True)

    assert response.status_code == 200


def test_view_feedback(client):
    # Insert test feedback directly into DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (name, message, is_read) VALUES (?, ?, 0)", ("Test User", "Test Message"))
    conn.commit()

    response = client.get('/feedback')
    assert response.status_code == 200


def test_export_feedback(client):
    # Insert sample data
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (name, message, is_read) VALUES (?, ?, 0)", ("Export User", "CSV test"))
    conn.commit()

    response = client.get('/export')
    assert response.status_code == 200

