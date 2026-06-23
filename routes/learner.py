import json
from flask import Blueprint, render_template, redirect, url_for
from database.db import get_connection

learner_bp = Blueprint("learner", __name__)


@learner_bp.route("/learner/<int:learner_id>")
def learner_profile(learner_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT l.name, l.attendance, l.daily_hours, a.performance_score, a.grade,
               a.status_level, a.improvement_areas, a.strengths, a.study_plan,
               a.recommendations
        FROM learners l
        JOIN analytics a ON l.id = a.learner_id
        WHERE l.id = %s
    """, (learner_id,))
    info = cursor.fetchone()

    if not info:
        cursor.close()
        db.close()
        return render_template("learner.html", info=None)

    cursor.execute("SELECT course_name, total_marks FROM learner_courses WHERE learner_id = %s", (learner_id,))
    rows = cursor.fetchall()
    cursor.close()
    db.close()

    courses = [r[0] for r in rows]
    scores = [r[1] for r in rows]
    study_plan = json.loads(info[8]) if info[8] else []
    recommendations = json.loads(info[9]) if info[9] else []

    return render_template(
        "learner.html",
        info=info,
        rows=rows,
        courses=json.dumps(courses),
        scores=json.dumps(scores),
        study_plan=study_plan,
        recommendations=recommendations
    )


@learner_bp.route("/remove/<int:learner_id>")
def remove_learner(learner_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM learner_courses WHERE learner_id = %s", (learner_id,))
    cursor.execute("DELETE FROM analytics WHERE learner_id = %s", (learner_id,))
    cursor.execute("DELETE FROM learners WHERE id = %s", (learner_id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("performance.performance_prediction"))
