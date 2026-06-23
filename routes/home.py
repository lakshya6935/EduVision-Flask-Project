import json
from flask import Blueprint, render_template
from database.db import get_connection

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def homepage():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT l.name, a.performance_score, a.status_level
        FROM learners l
        JOIN analytics a ON l.id = a.learner_id
        ORDER BY a.performance_score DESC
    """)
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    best_score = rows[0][1] if rows else 0
    average_score = round(sum(r[1] for r in rows) / len(rows), 2) if rows else 0
    low_risk = sum(1 for r in rows if "Low" in r[2])
    medium_risk = sum(1 for r in rows if "Medium" in r[2])
    high_risk = sum(1 for r in rows if "High" in r[2])

    names = [r[0] for r in rows[:10]]
    scores = [r[1] for r in rows[:10]]

    return render_template(
        "home.html",
        best_score=best_score,
        average_score=average_score,
        low_risk=low_risk,
        medium_risk=medium_risk,
        high_risk=high_risk,
        names=json.dumps(names),
        scores=json.dumps(scores)
    )
