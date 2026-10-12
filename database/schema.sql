-- =====================================================
-- Placement Preparation Tracker - MySQL schema
-- Run this whole file in MySQL Workbench (lightning bolt).
-- Safe to re-run: it drops and recreates the tables
-- (this DELETES existing data, so only use it early on).
-- =====================================================

CREATE DATABASE IF NOT EXISTS placement_tracker;
USE placement_tracker;

-- Drop in reverse order of dependency so foreign keys don't complain
DROP TABLE IF EXISTS offers;
DROP TABLE IF EXISTS interview_feedback;
DROP TABLE IF EXISTS test_scores;
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS job_departments;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS users;

-- 1. USERS: login details and role
CREATE TABLE users (
    user_id        INT AUTO_INCREMENT PRIMARY KEY,
    username       VARCHAR(50)  NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    role           ENUM('Student', 'TPO') NOT NULL
);

-- 2. STUDENTS: profile info (a TPO user has no student row)
CREATE TABLE students (
    student_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT UNIQUE,                       -- UNIQUE gives the 1 : 0..1 link
    roll_no      VARCHAR(20)  NOT NULL UNIQUE,
    name         VARCHAR(100) NOT NULL,
    email        VARCHAR(100) NOT NULL UNIQUE,
    department   VARCHAR(50)  NOT NULL,
    cgpa         DECIMAL(4,2) NOT NULL,
    skills       TEXT,                             -- e.g. 'Python, SQL, Java'
    resume_path  VARCHAR(255),
    CONSTRAINT chk_cgpa CHECK (cgpa BETWEEN 0 AND 10),
    CONSTRAINT fk_students_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE SET NULL
);

-- 3. COMPANIES
CREATE TABLE companies (
    company_id    INT AUTO_INCREMENT PRIMARY KEY,
    company_name  VARCHAR(100) NOT NULL UNIQUE,
    address       VARCHAR(255),
    website       VARCHAR(150)
);

-- 4. JOBS: listings and eligibility requirements
CREATE TABLE jobs (
    job_id      INT AUTO_INCREMENT PRIMARY KEY,
    company_id  INT NOT NULL,
    job_role    VARCHAR(100) NOT NULL,
    package     DECIMAL(6,2),                      -- in LPA
    min_cgpa    DECIMAL(4,2) NOT NULL DEFAULT 0,
    visit_date  DATE,
    CONSTRAINT chk_min_cgpa CHECK (min_cgpa BETWEEN 0 AND 10),
    CONSTRAINT fk_jobs_company
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
        ON DELETE CASCADE
);

-- 4b. JOB_DEPARTMENTS: which departments are eligible for a job
--     (the design doc suggests this for department eligibility checking)
CREATE TABLE job_departments (
    job_id      INT NOT NULL,
    department  VARCHAR(50) NOT NULL,
    PRIMARY KEY (job_id, department),
    CONSTRAINT fk_jobdept_job
        FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        ON DELETE CASCADE
);

-- 5. APPLICATIONS: a student applying to a job
CREATE TABLE applications (
    application_id  INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT NOT NULL,
    job_id          INT NOT NULL,
    applied_date    DATE NOT NULL DEFAULT (CURRENT_DATE),
    status          ENUM('Applied', 'Shortlisted', 'Selected', 'Rejected')
                    NOT NULL DEFAULT 'Applied',
    CONSTRAINT uq_student_job UNIQUE (student_id, job_id),   -- no duplicate applications
    CONSTRAINT fk_app_student
        FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_app_job
        FOREIGN KEY (job_id) REFERENCES jobs(job_id)
        ON DELETE CASCADE
);

-- 6. TEST_SCORES: mock test results
CREATE TABLE test_scores (
    score_id    INT AUTO_INCREMENT PRIMARY KEY,
    student_id  INT NOT NULL,
    test_name   VARCHAR(100) NOT NULL,             -- Aptitude / Coding / Technical
    score       DECIMAL(5,2) NOT NULL,
    test_date   DATE,
    CONSTRAINT chk_score CHECK (score >= 0),
    CONSTRAINT fk_score_student
        FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE
);

-- 7. INTERVIEW_FEEDBACK: one row per interview round
CREATE TABLE interview_feedback (
    feedback_id     INT AUTO_INCREMENT PRIMARY KEY,
    application_id  INT NOT NULL,
    round_name      VARCHAR(100) NOT NULL,
    feedback        TEXT,
    result          ENUM('Pending', 'Cleared', 'Not Cleared') NOT NULL DEFAULT 'Pending',
    CONSTRAINT fk_feedback_app
        FOREIGN KEY (application_id) REFERENCES applications(application_id)
        ON DELETE CASCADE
);

-- 8. OFFERS: at most one offer per application
CREATE TABLE offers (
    offer_id           INT AUTO_INCREMENT PRIMARY KEY,
    application_id     INT NOT NULL UNIQUE,        -- UNIQUE gives the 1 : 0..1 link
    offer_package      DECIMAL(6,2),               -- in LPA
    offer_date         DATE,
    offer_letter_path  VARCHAR(255),
    status             ENUM('Offered', 'Accepted', 'Declined') NOT NULL DEFAULT 'Offered',
    CONSTRAINT fk_offer_app
        FOREIGN KEY (application_id) REFERENCES applications(application_id)
        ON DELETE CASCADE
);

-- Quick check: should list all 9 tables
SHOW TABLES;
