from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_cors import CORS
import os
import psycopg2
import sqlite3
import csv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "test_secret_key")

# ---------------------------------------------------------
# ✅ Database Connection: Switch between PostgreSQL and SQLite
# ---------------------------------------------------------
def get_db_connection():
    if app.config.get("TESTING"):
        # Use in-memory SQLite for tests
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                message TEXT,
                is_read BOOLEAN DEFAULT 0
            )
        """)
        conn.commit()
        return conn
    else:
        # Use PostgreSQL for production / development
        return psycopg2.connect(
            host=os.getenv("PGHOST"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            database=os.getenv("PGDATABASE")
        )

# Create connection and cursor
conn = get_db_connection()
cursor = conn.cursor()

# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name') or None
        message = request.form.get('message')

        if not message:
            flash('Message is required.')
            return redirect(url_for('index'))

        try:
            cursor.execute("INSERT INTO feedback (name, message, is_read) VALUES (?, ?, 0)" if app.config.get("TESTING")
                           else "INSERT INTO feedback (name, message, is_read) VALUES (%s, %s, false)",
                           (name, message))
            conn.commit()
            return redirect(url_for('thank_you'))
        except Exception as e:
            conn.rollback()
            app.logger.error("Error inserting feedback: %s", e)
            flash('Failed to submit feedback.')
            return redirect(url_for('index'))

    return render_template('index.html')


@app.route('/feedback')
def view_feedback():
    cursor.execute("SELECT id, name, message, is_read FROM feedback ORDER BY id DESC")
    feedbacks = cursor.fetchall()
    return render_template('feedback.html', feedbacks=feedbacks)


@app.route('/feedback/read/<int:id>')
def mark_as_read(id):
    cursor.execute("UPDATE feedback SET is_read = 1 WHERE id = ?" if app.config.get("TESTING")
                   else "UPDATE feedback SET is_read = true WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('view_feedback'))


@app.route('/feedback/delete/<int:id>')
def delete_feedback(id):
    cursor.execute("DELETE FROM feedback WHERE id = ?" if app.config.get("TESTING")
                   else "DELETE FROM feedback WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('view_feedback'))


@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/export')
def export_feedback():
    cursor.execute("SELECT id, name, message, is_read FROM feedback ORDER BY id")
    feedbacks = cursor.fetchall()

    filename = "feedback_export.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Name", "Message", "Is Read"])
        for row in feedbacks:
            writer.writerow(row)

    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
