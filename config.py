"""
Configuration file for Placement Portal
Update the database credentials according to your MySQL setup
"""

import os
from datetime import timedelta

class Config:
    # Secret key for session management (CHANGE THIS IN PRODUCTION)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MySQL Database Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'  # Change to your MySQL username
    MYSQL_PASSWORD = ''  # Change to your MySQL password
    MYSQL_DB = 'placement_portal'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # File Upload Configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Session Configuration
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_TYPE = 'filesystem'
    
    # ML Models Path
    PLACEMENT_MODEL_PATH = 'placement_model.pkl'
    SALARY_MODEL_PATH = 'salary_model.pkl'
    
    # Skill Keywords for Resume Parsing
    SKILL_KEYWORDS = [
        # Programming Languages
        'Python', 'Java', 'JavaScript', 'C++', 'C', 'C#', 'Ruby', 'Go', 'Rust',
        'PHP', 'Swift', 'Kotlin', 'TypeScript', 'Scala', 'R', 'MATLAB',
        
        # Web Technologies
        'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js',
        'Django', 'Flask', 'Spring Boot', 'ASP.NET', 'Bootstrap', 'jQuery',
        'REST API', 'GraphQL', 'AJAX',
        
        # Databases
        'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle', 'SQL Server',
        'Redis', 'Cassandra', 'DynamoDB', 'Firebase',
        
        # Data Science & ML
        'Machine Learning', 'Deep Learning', 'Neural Networks', 'TensorFlow',
        'PyTorch', 'Keras', 'scikit-learn', 'Pandas', 'NumPy', 'Data Analysis',
        'Data Science', 'NLP', 'Computer Vision', 'AI',
        
        # Cloud & DevOps
        'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'CI/CD',
        'Jenkins', 'Git', 'GitHub', 'GitLab', 'Linux', 'Shell Scripting',
        
        # Other Technologies
        'Data Structures', 'Algorithms', 'DSA', 'OOP', 'System Design',
        'Microservices', 'Blockchain', 'IoT', 'Cybersecurity', 'Testing',
        'Agile', 'Scrum', 'JIRA'
    ]
    
    # Important skills for different branches
    BRANCH_IMPORTANT_SKILLS = {
        'Computer Science': ['Python', 'Java', 'Data Structures', 'Algorithms', 'SQL', 'Git'],
        'Information Technology': ['JavaScript', 'HTML', 'CSS', 'SQL', 'Python', 'Git'],
        'Electronics': ['Python', 'C', 'C++', 'MATLAB', 'Embedded Systems'],
        'Mechanical': ['CAD', 'MATLAB', 'Python', 'Simulation'],
        'Civil': ['AutoCAD', 'STAAD Pro', 'Python', 'Data Analysis'],
        'Electrical': ['MATLAB', 'Python', 'PLC', 'SCADA']
    }
    
    # Risk level thresholds
    RISK_THRESHOLDS = {
        'Low': 70,      # >= 70% probability = Low risk
        'Medium': 40,   # 40-70% = Medium risk
        'High': 0       # < 40% = High risk
    }
    
    # Pagination
    PREDICTIONS_PER_PAGE = 10
    
    # Admin credentials (for initial setup)
    DEFAULT_ADMIN_EMAIL = 'admin@placement.com'
    DEFAULT_ADMIN_PASSWORD = 'admin123'  # CHANGE THIS!
