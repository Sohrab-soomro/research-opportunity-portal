-- Optional demo data. Each run adds two rows.
USE research_portal;
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
