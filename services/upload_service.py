import json
import statistics
import pandas as pd

from database.db import get_connection
from model.predictor import predict_score
from services.analysis import analyze_learner


def process_uploaded_file(file):
    if file.filename.lower().endswith(".csv"):
        df = pd.read_csv(file)
    elif file.filename.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
    else:
        raise ValueError("Only CSV or Excel files are allowed.")

    df.columns = df.columns.str.strip().str.lower()

    required_columns = ["name", "attendance", "daily_available_hours"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column missing: {col}")

    db = get_connection()
    cursor = db.cursor()

    for _, row in df.iterrows():
        learner_name = str(row["name"])
        attendance = float(row["attendance"])
        daily_hours = float(row["daily_available_hours"])

        cursor.execute(
            "INSERT INTO learners (name, attendance, daily_hours) VALUES (%s, %s, %s)",
            (learner_name, attendance, daily_hours)
        )

        learner_id = cursor.lastrowid
        courses = {}
        course_names = set()

        for col in df.columns:
            if col.endswith("_internal"):
                course_names.add(col.replace("_internal", ""))

        for course in course_names:
            internal = float(row.get(f"{course}_internal", 0))
            external = float(row.get(f"{course}_external", 0))
            assignment = float(row.get(f"{course}_assignment", 0))
            total = internal + external + assignment

            courses[course] = total

            cursor.execute("""
                INSERT INTO learner_courses
                (learner_id, course_name, internal_marks, external_marks, assignment_marks, total_marks)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (learner_id, course, internal, external, assignment, total))

        if not courses:
            continue

        course_scores = list(courses.values())
        average_marks = sum(course_scores) / len(course_scores)
        lowest_marks = min(course_scores)
        highest_marks = max(course_scores)
        consistency = 100

        if len(course_scores) > 1:
            consistency = max(0, 100 - statistics.stdev(course_scores))

        features = [[attendance, average_marks, lowest_marks, highest_marks, consistency, 70]]
        predicted_score = predict_score(features)
        result = analyze_learner(attendance, daily_hours, courses)

        improvement_areas = ", ".join(result["weak"]) if result["weak"] else "None"
        strengths = ", ".join(result["strong"]) if result["strong"] else "None"

        cursor.execute("""
            INSERT INTO analytics
            (learner_id, performance_score, grade, status_level, improvement_areas, strengths, study_plan, recommendations)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            learner_id,
            round(predicted_score, 2),
            result["grade"],
            result["risk"],
            improvement_areas,
            strengths,
            json.dumps(result["timetable"]),
            json.dumps(result["suggestions"])
        ))

    db.commit()
    cursor.close()
    db.close()
