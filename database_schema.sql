-- ================================================
-- PLACEMENT PORTAL DATABASE SCHEMA
-- ================================================
-- Database: placement_portal
-- Created: March 2026
-- ================================================

CREATE DATABASE IF NOT EXISTS placement_portal;
USE placement_portal;

-- ================================================
-- 1. USERS TABLE (Authentication)
-- ================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    user_type ENUM('student', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_user_type (user_type)
);

-- ================================================
-- 2. STUDENT PROFILES TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS student_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    enrollment_number VARCHAR(50) UNIQUE,
    branch VARCHAR(100) NOT NULL,
    cgpa DECIMAL(3,2) NOT NULL CHECK (cgpa >= 0 AND cgpa <= 10),
    semester INT CHECK (semester BETWEEN 1 AND 8),
    internship_count INT DEFAULT 0,
    project_count INT DEFAULT 0,
    certification_count INT DEFAULT 0,
    skills TEXT,  -- Stored as comma-separated values
    phone VARCHAR(15),
    alternate_email VARCHAR(255),
    github_url VARCHAR(255),
    linkedin_url VARCHAR(255),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_branch (branch),
    INDEX idx_cgpa (cgpa)
);

-- ================================================
-- 3. PREDICTIONS TABLE (ML Results History)
-- ================================================
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    placement_probability DECIMAL(5,2) NOT NULL,
    predicted_salary DECIMAL(10,2),
    risk_level ENUM('Low', 'Medium', 'High') NOT NULL,
    cgpa DECIMAL(3,2) NOT NULL,
    branch VARCHAR(100) NOT NULL,
    internship_count INT,
    project_count INT,
    certification_count INT,
    skills_used TEXT,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_predictions (user_id, prediction_date),
    INDEX idx_prediction_date (prediction_date)
);

-- ================================================
-- 4. RESUME DATA TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS resume_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    extracted_skills TEXT,
    extracted_text TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_resume (user_id)
);

-- ================================================
-- 5. SKILL GAP ANALYSIS TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS skill_gaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    missing_skills TEXT,
    recommended_actions TEXT,
    priority ENUM('High', 'Medium', 'Low') DEFAULT 'Medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_gaps (user_id)
);

-- ================================================
-- 6. WHAT-IF SIMULATIONS TABLE
-- ================================================
CREATE TABLE IF NOT EXISTS simulations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    original_probability DECIMAL(5,2),
    simulated_probability DECIMAL(5,2),
    changes_made TEXT,  -- JSON format storing what changed
    simulation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_simulations (user_id)
);

-- ================================================
-- 7. ADMIN STATISTICS TABLE (Cached Analytics)
-- ================================================
CREATE TABLE IF NOT EXISTS admin_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stat_name VARCHAR(100) UNIQUE NOT NULL,
    stat_value TEXT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ================================================
-- INSERT DEFAULT ADMIN USER
-- ================================================
-- Password: admin123 (hashed using werkzeug.security)
-- You'll need to update this hash after running the app
INSERT INTO users (email, password_hash, full_name, user_type) 
VALUES ('admin@placement.com', 'pbkdf2:sha256:placeholder', 'Admin User', 'admin')
ON DUPLICATE KEY UPDATE email=email;

-- ================================================
-- SAMPLE DATA FOR TESTING
-- ================================================

-- Sample Student Users
INSERT INTO users (email, password_hash, full_name, user_type) VALUES
('student1@college.com', 'pbkdf2:sha256:placeholder', 'Rahul Sharma', 'student'),
('student2@college.com', 'pbkdf2:sha256:placeholder', 'Priya Patel', 'student'),
('student3@college.com', 'pbkdf2:sha256:placeholder', 'Amit Kumar', 'student')
ON DUPLICATE KEY UPDATE email=email;

-- Sample Student Profiles
INSERT INTO student_profiles (user_id, enrollment_number, branch, cgpa, semester, internship_count, project_count, certification_count, skills) VALUES
(2, 'EN2022001', 'Computer Science', 8.5, 8, 2, 3, 2, 'Python,Java,SQL,Machine Learning,React'),
(3, 'EN2022002', 'Information Technology', 7.8, 8, 1, 2, 1, 'JavaScript,HTML,CSS,Node.js,MongoDB'),
(4, 'EN2022003', 'Electronics', 9.0, 8, 3, 4, 3, 'Python,C++,MATLAB,Data Science,Deep Learning')
ON DUPLICATE KEY UPDATE enrollment_number=enrollment_number;

-- ================================================
-- VIEWS FOR ANALYTICS
-- ================================================

-- Branch-wise average placement probability
CREATE OR REPLACE VIEW branch_placement_stats AS
SELECT 
    sp.branch,
    COUNT(DISTINCT p.user_id) as total_students,
    AVG(p.placement_probability) as avg_probability,
    AVG(p.predicted_salary) as avg_salary
FROM student_profiles sp
LEFT JOIN predictions p ON sp.user_id = p.user_id
GROUP BY sp.branch;

-- Recent predictions view
CREATE OR REPLACE VIEW recent_predictions AS
SELECT 
    u.full_name,
    u.email,
    sp.branch,
    p.placement_probability,
    p.predicted_salary,
    p.risk_level,
    p.prediction_date
FROM predictions p
JOIN users u ON p.user_id = u.id
JOIN student_profiles sp ON p.user_id = sp.user_id
ORDER BY p.prediction_date DESC
LIMIT 100;

-- ================================================
-- STORED PROCEDURE: Get Student Dashboard Data
-- ================================================
DELIMITER //

CREATE PROCEDURE GetStudentDashboard(IN student_user_id INT)
BEGIN
    -- Get student profile
    SELECT * FROM student_profiles WHERE user_id = student_user_id;
    
    -- Get recent predictions
    SELECT * FROM predictions 
    WHERE user_id = student_user_id 
    ORDER BY prediction_date DESC 
    LIMIT 10;
    
    -- Get latest skill gap
    SELECT * FROM skill_gaps 
    WHERE user_id = student_user_id 
    ORDER BY created_at DESC 
    LIMIT 1;
END //

DELIMITER ;

-- ================================================
-- END OF SCHEMA
-- ================================================
