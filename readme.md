
# 📝 Student Feedback App – Kanban-Based DevOps Project

This is a **student feedback application** built with **Flask** and **PostgreSQL**, designed to teach Agile principles using **User Stories**, **GitHub Issues**, and a **Kanban board**.

## 🚀 Project Goal

To simulate an Agile development process using 10 user stories that cover both frontend and backend functionality, database interaction, and deployment.

---

## 📋 User Stories Breakdown & Implementation

### ✅ User Story 1 & 2
**As a student**, I want to submit feedback with a message field,  
**and** submit feedback anonymously, so I can speak freely.

🔹 **Code:**  
- `index.html` contains a form with optional `name` and required `message` fields.  
- If no name is provided or "anonymous" is checked, feedback is submitted anonymously.

📍Code:
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        if request.form.get('anonymous'):
            name = None
        ...
```
📄 Template: `index.html`

---

### ✅ User Story 3  
**As a teacher**, I want to view all feedback so I can understand students' thoughts.

🔹 **Code:**  
Route `/feedback` fetches all feedback from the database and renders it.

📍Code:
```python
@app.route('/feedback')
def view_feedback():
    cursor.execute("SELECT id, name, message, is_read FROM feedback ORDER BY submitted_at DESC")
    feedbacks = cursor.fetchall()
    return render_template('feedback.html', feedbacks=feedbacks)
```

---

### ✅ User Story 4  
**As a teacher**, I want to mark a feedback message as read.

🔹 **Code:**  
A button in `feedback.html` calls `/feedback/read/<id>` to update the `is_read` field.

📍Code:
```python
@app.route('/feedback/read/<int:id>')
def mark_as_read(id):
    cursor.execute("UPDATE feedback SET is_read = true WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('view_feedback'))
```

---

### ✅ User Story 5  
**As a teacher**, I want to delete feedback.

🔹 **Code:**  
`/feedback/delete/<id>` removes a feedback entry from the database.

📍Code:
```python
@app.route('/feedback/delete/<int:id>')
def delete_feedback(id):
    cursor.execute("DELETE FROM feedback WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('view_feedback'))
```

---

### ✅ User Story 6  
**As a user**, I want the app to store feedback in a database.

🔹 **Code:**  
PostgreSQL is used for persistence. Connection is established via `.env`.

📍Code:
```python
conn = psycopg2.connect(
    host=os.getenv("PGHOST"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    database=os.getenv("PGDATABASE")
)
```

🛠 **SQL to create the `feedback` table:**
```sql
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    name TEXT,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### ✅ User Story 7  
**As a user**, I want a clean UI so the app is easy to use.

🔹 **Code:**  
Clean HTML5-based templates using Jinja2.

📄 Templates:  
- `base.html` – Shared layout  
- `index.html` – Submit form  
- `thank_you.html` – Thank you message  
- `feedback.html` – Admin interface

---

### ✅ User Story 8  
**As a developer**, I want to write tests.

🔹 **Tests can be added** using `pytest` or `unittest`, for example:
```python
def test_home_status_code(client):
    response = client.get('/')
    assert response.status_code == 200
```

---

### ✅ User Story 9  
**As a teacher**, I want to export all feedback.

🔹 **Code:**  
`/export` endpoint creates a CSV file and returns it for download.

📍Code:
```python
@app.route('/export')
def export_feedback():
    ...
    return send_file(filename, as_attachment=True)
```

---

### ✅ User Story 10  
**As a user**, I want the app deployed online.

🔹 **Deployment:** Done using [Render](https://render.com/), with environment variables configured in the dashboard.

📍File:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🛠 Project Setup

### 🧪 Requirements
- Python 3.10+
- PostgreSQL (or cloud DB like Vercel Neon)
- Flask
- psycopg2-binary
- python-dotenv

### 📦 Installation
```bash
pip install -r requirements.txt
```

### 🌐 .env Example
```
PGHOST=your-host
PGUSER=your-username
PGPASSWORD=your-password
PGDATABASE=your-database
```

---

## 💡 GitHub Kanban / Issues

Use these user stories to:
- Create GitHub Issues with `feature`, `bug`, or `task` labels.
- Track them on a GitHub Project Kanban board under **To Do**, **In Progress**, and **Done**.

Each story can be one issue, e.g.:
- 🟩 `[US1] Feedback form with name/message`
- 🟨 `[US3] View feedback page for teacher`
- 🟥 `[US5] Delete feedback route`

---

## ✅ What You Can Demonstrate in Class

| Topic            | Covered? |
|------------------|----------|
| Agile User Stories | ✅ |
| GitHub Kanban    | ✅ |
| Issue Tracking   | ✅ |
| Python/Flask Dev | ✅ |
| PostgreSQL Setup | ✅ |
| Deployment (Render) | ✅ |
