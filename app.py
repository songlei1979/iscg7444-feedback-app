from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
import csv

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
CORS(app)

# PostgreSQL connection
conn = psycopg2.connect(
    host=os.getenv("PGHOST"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    database=os.getenv("PGDATABASE")
)
cursor = conn.cursor()

# ---------- USER STORY 1 & 2 ----------
# As a student, I want to submit feedback with a message field
# As a student, I want to submit feedback anonymously
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name') or None
        message = request.form.get('message')

        if not message:
            flash('Message is required.')
            return redirect(url_for('index'))

        try:
            print(name, message)
            cursor.execute("INSERT INTO feedback (name, message, is_read) VALUES (%s, %s, false)", (name, message))
            conn.commit()
            return redirect(url_for('thank_you'))
        except Exception as e:
            conn.rollback()  # This is the key fix
            app.logger.error("Error inserting feedback: %s", e)
            flash('Failed to submit feedback.')
            return redirect(url_for('index'))

    return render_template('index.html')

# ---------- USER STORY 3 ----------
# As a teacher, I want to view all feedback
@app.route('/feedback')
def view_feedback():
    cursor.execute("SELECT id, name, message, is_read FROM feedback ORDER BY submitted_at DESC")
    feedbacks = cursor.fetchall()
    print(feedbacks)
    return render_template('feedback.html', feedbacks=feedbacks)

# ---------- USER STORY 4 ----------
# As a teacher, I want to mark a feedback message as read
@app.route('/feedback/read/<int:id>')
def mark_as_read(id):
    cursor.execute("UPDATE feedback SET is_read = true WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('view_feedback'))

# ---------- USER STORY 5 ----------
# As a teacher, I want to delete feedback
@app.route('/feedback/delete/<int:id>')
def delete_feedback(id):
    cursor.execute("DELETE FROM feedback WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('view_feedback'))

# ---------- USER STORY 6 ----------
# As a user, I want the app to store feedback in a database
# (Handled by PostgreSQL + .env connection)

# ---------- USER STORY 7 ----------
# As a user, I want a clean UI
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# ---------- USER STORY 9 ----------
# As a teacher, I want to export all feedback
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

# ---------- USER STORY 10 ----------
# As a user, I want the app deployed online
# (Deployment would be handled via Render or similar platform)

# ---------- USER STORY 8 ----------
# As a developer, I want to write tests (not shown here, add in separate test file)

if __name__ == '__main__':
    app.run(debug=True)
