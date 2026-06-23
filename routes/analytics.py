import json
from flask import Blueprint, render_template
from database.db import get_connection

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
def analytics_dashboard():
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT l.id, l.name, l.attendance, a.performance_score, a.grade,
               a.status_level, a.improvement_areas, a.strengths
        FROM learners l
        JOIN analytics a ON l.id = a.learner_id
        ORDER BY a.performance_score DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    db.close()

    total_learners = len(data)
    average_score = round(sum(r[3] for r in data) / total_learners, 2) if total_learners else 0
    average_attendance = round(sum(r[2] for r in data) / total_learners, 2) if total_learners else 0
    high_risk = sum(1 for r in data if "High" in r[5])
    low_risk = sum(1 for r in data if "Low" in r[5])

    grade_count = {}
    weak_count = {}
    strong_count = {}

    for row in data:
        grade_count[row[4]] = grade_count.get(row[4], 0) + 1
        if row[6] != "None":
            for course in row[6].split(", "):
                weak_count[course] = weak_count.get(course, 0) + 1
        if row[7] != "None":
            for course in row[7].split(", "):
                strong_count[course] = strong_count.get(course, 0) + 1

    top_name = data[0][1] if data else "N/A"
    top_score = data[0][3] if data else 0
    most_weak_course = max(weak_count, key=weak_count.get) if weak_count else "N/A"
    best_course = max(strong_count, key=strong_count.get) if strong_count else "N/A"
    class_advice = f"Extra focus recommended in {most_weak_course}"

    return render_template(
        "analytics.html",
        data=data,
        total_learners=total_learners,
        average_score=average_score,
        average_attendance=average_attendance,
        high_risk=high_risk,
        low_risk=low_risk,
        top_name=top_name,
        top_score=top_score,
        most_weak_course=most_weak_course,
        best_course=best_course,
        class_advice=class_advice,
        grade_labels=json.dumps(list(grade_count.keys())),
        grade_values=json.dumps(list(grade_count.values()))
    )
