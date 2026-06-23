import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection(database=True):
    if database:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_database():
    # Create database first, then create required tables.
    server_db = get_connection(database=False)
    server_cursor = server_db.cursor()
    server_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    server_db.commit()
    server_cursor.close()
    server_db.close()

    db = get_connection()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learners (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            attendance FLOAT NOT NULL,
            daily_hours FLOAT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learner_courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            learner_id INT NOT NULL,
            course_name VARCHAR(100) NOT NULL,
            internal_marks FLOAT DEFAULT 0,
            external_marks FLOAT DEFAULT 0,
            assignment_marks FLOAT DEFAULT 0,
            total_marks FLOAT DEFAULT 0,
            FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            learner_id INT NOT NULL,
            performance_score FLOAT NOT NULL,
            grade VARCHAR(10),
            status_level VARCHAR(50),
            improvement_areas TEXT,
            strengths TEXT,
            study_plan TEXT,
            recommendations TEXT,
            FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
        )
    """)

    db.commit()
    cursor.close()
    db.close()
