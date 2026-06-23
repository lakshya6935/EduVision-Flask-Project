# EduVision - Flask Academic Performance System

This is the separated, ready-to-run version of the EduVision one-file Flask project.

## Project Linking

- `app.py` creates the Flask app and registers all route files.
- `routes/*.py` contains page URLs.
- `database/db.py` connects MySQL and creates database/tables.
- `services/analysis.py` contains grade, risk, weak subject, and recommendation logic.
- `services/upload_service.py` reads CSV/Excel and saves data.
- `model/predictor.py` loads `model/model.pkl`. If it is missing, fallback prediction is used.
- `templates/*.html` contains HTML pages.
- `static/css/style.css` contains design.
- `static/js/charts.js` contains chart functions.

## Folder Structure

```text
EduVision_Project/
├── app.py
├── config.py
├── requirements.txt
├── sample_data.csv
├── database/
│   ├── db.py
│   └── schema.sql
├── model/
│   └── predictor.py
├── routes/
│   ├── home.py
│   ├── upload.py
│   ├── analytics.py
│   ├── performance.py
│   └── learner.py
├── services/
│   ├── analysis.py
│   └── upload_service.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── upload.html
│   ├── analytics.html
│   ├── performance.html
│   └── learner.html
└── static/
    ├── css/style.css
    ├── js/charts.js
    └── uploads/
```

## How to Run

### 1. Install Python packages

```bash
pip install -r requirements.txt
```

### 2. Start MySQL

Make sure MySQL server is running.

Default database settings are in `config.py`:

```python
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "eduvision"
```

Change password if your MySQL has a password.

### 3. Run the project

```bash
python app.py
```

### 4. Open in browser

```text
http://127.0.0.1:5000
```

### 5. Upload sample data

Use `sample_data.csv` from this folder on the Upload Data page.

## CSV Format

Required columns:

```text
name, attendance, daily_available_hours
```

Subject columns format:

```text
subject_internal, subject_external, subject_assignment
```

Example:

```text
python_internal, python_external, python_assignment
```
