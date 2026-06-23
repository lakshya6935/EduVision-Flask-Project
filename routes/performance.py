from flask import Blueprint, render_template, request, redirect, url_for
from database.db import get_connection

performance_bp = Blueprint("performance", __name__)


@performance_bp.route("/performance")
def performance_prediction():
    search = request.args.get("search", "")
    status = request.args.get("status", "")
    grade = request.args.get("grade", "")
    sort = request.args.get("sort", "desc")

    query = """
        SELECT l.id, l.name, a.performance_score, a.grade, a.status_level,
               a.improvement_areas, a.strengths
        FROM learners l
        JOIN analytics a ON l.id = a.learner_id
        WHERE 1=1
    """
    values = []

    if search:
        query += " AND l.name LIKE %s"
        values.append(f"%{search}%")
    if status:
        query += " AND a.status_level LIKE %s"
        values.append(f"%{status}%")
    if grade:
        query += " AND a.grade = %s"
        values.append(grade)

    query += " ORDER BY a.performance_score ASC" if sort == "asc" else " ORDER BY a.performance_score DESC"

    db = get_connection()
    cursor = db.cursor()
    cursor.execute(query, values)
    data = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("performance.html", data=data, search=search, status=status, grade=grade, sort=sort)


@performance_bp.route("/remove_selected", methods=["POST"])
def remove_selected_learners():
    learner_ids = request.form.getlist("learner_ids")
    db = get_connection()
    cursor = db.cursor()

    for learner_id in learner_ids:
        cursor.execute("DELETE FROM learner_courses WHERE learner_id = %s", (learner_id,))
        cursor.execute("DELETE FROM analytics WHERE learner_id = %s", (learner_id,))
        cursor.execute("DELETE FROM learners WHERE id = %s", (learner_id,))

    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("performance.performance_prediction"))
