CREATE DATABASE IF NOT EXISTS eduvision;
USE eduvision;

CREATE TABLE IF NOT EXISTS learners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    attendance FLOAT NOT NULL,
    daily_hours FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS learner_courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    learner_id INT NOT NULL,
    course_name VARCHAR(100) NOT NULL,
    internal_marks FLOAT DEFAULT 0,
    external_marks FLOAT DEFAULT 0,
    assignment_marks FLOAT DEFAULT 0,
    total_marks FLOAT DEFAULT 0,
    FOREIGN KEY (learner_id) REFERENCES learners(id) ON DELETE CASCADE
);

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
);
