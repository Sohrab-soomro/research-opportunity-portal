-- ==========================================================
-- University Research Opportunity Portal - Database Schema
-- Run this file once in MySQL to create the database and table.
-- ==========================================================

CREATE DATABASE IF NOT EXISTS research_portal;
USE research_portal;

CREATE TABLE IF NOT EXISTS opportunities (
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
