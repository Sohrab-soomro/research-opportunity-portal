-- ==========================================================
-- University Research Opportunity Portal - Database Schema
-- Run this file once in MySQL to create the database and table.
-- ==========================================================

CREATE DATABASE IF NOT EXISTS research_portal;
USE research_portal;

DROP TABLE IF EXISTS opportunities;

CREATE TABLE opportunities (
    id                   INT AUTO_INCREMENT PRIMARY KEY,      -- Unique ID
    research_title       VARCHAR(200)  NOT NULL,
    research_description TEXT          NOT NULL,
    research_area        VARCHAR(100)  NOT NULL,
    faculty_name         VARCHAR(100)  NOT NULL,
    department           VARCHAR(100)  NOT NULL,
    required_skills      VARCHAR(255)  NOT NULL,
    available_positions  INT           NOT NULL,
    application_deadline DATE          NOT NULL,
    status               ENUM('Open', 'Closed') NOT NULL DEFAULT 'Open',

    CONSTRAINT chk_positions CHECK (available_positions > 0)
);

-- Optional seed data (the frontend still loads these through the API)
INSERT INTO opportunities
    (research_title, research_description, research_area, faculty_name,
     department, required_skills, available_positions, application_deadline, status)
VALUES
    ('Network Traffic Classification using Machine Learning',
     'Classify encrypted network traffic flows using supervised learning models on public datasets.',
     'Computer Networks', 'Dr. Ayesha Khan', 'Computer Science',
     'Python, Wireshark, Machine Learning basics', 2, '2026-11-30', 'Open'),
    ('Urdu Text Summarization',
     'Build and evaluate an extractive summarization system for Urdu news articles.',
     'Natural Language Processing', 'Dr. Imran Ali', 'Computer Science',
     'Python, NLP, Data Cleaning', 3, '2026-12-15', 'Open');
