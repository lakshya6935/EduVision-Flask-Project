def analyze_learner(attendance, daily_hours, courses):
    scores = list(courses.values())
    average = sum(scores) / len(scores) if scores else 0

    weak = [subject for subject, marks in courses.items() if marks < 50]
    strong = [subject for subject, marks in courses.items() if marks >= 75]

    if average >= 85:
        grade = "A+"
    elif average >= 75:
        grade = "A"
    elif average >= 65:
        grade = "B"
    elif average >= 50:
        grade = "C"
    else:
        grade = "D"

    if attendance < 60 or average < 45:
        risk = "High Risk"
    elif attendance < 75 or average < 60:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    study_plan = []
    if weak:
        for subject in weak:
            study_plan.append({
                "day": subject.upper(),
                "task": f"Study {subject} for {max(1, round(daily_hours / max(1, len(weak)), 1))} hours"
            })
    else:
        study_plan.append({
            "day": "REVISION",
            "task": "Revise all subjects and practice previous questions"
        })

    recommendations = []
    if attendance < 75:
        recommendations.append("Improve attendance to reduce academic risk.")

    if weak:
        recommendations.append("Focus more on weak subjects: " + ", ".join(weak))
    else:
        recommendations.append("Performance is good. Continue regular revision.")

    if daily_hours < 2:
        recommendations.append("Increase daily study time to at least 2 hours.")

    return {
        "grade": grade,
        "risk": risk,
        "weak": weak,
        "strong": strong,
        "timetable": study_plan,
        "suggestions": recommendations
    }
