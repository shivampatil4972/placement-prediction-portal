"""
Configuration file for Placement Portal
Update the database credentials according to your MySQL setup
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MySQL Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'placement_portal')
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    PROFILE_PIC_FOLDER = os.path.join(UPLOAD_FOLDER, 'profiles')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    ALLOWED_EXTENSIONS = {'pdf'}
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
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
    DEFAULT_ADMIN_EMAIL = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@placement.com')
    DEFAULT_ADMIN_PASSWORD = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'admin123')
