# Student Placement Prediction & Strategy Portal

## 📋 Project Overview

A comprehensive web-based platform that leverages Machine Learning to predict student placement probability, estimate expected salary, analyze skill gaps, and provide personalized recommendations for career improvement.

### 🎯 Project Type
**Final Year Engineering Project**

### 👥 Target Users
- Engineering students preparing for campus placements
- College placement officers and administrators
- Career counselors

---

## ✨ Key Features

### 1. **Authentication System**
- Student registration and login
- Admin panel access
- Secure password hashing
- Session management

### 2. **Student Profile Management**
- Academic information (CGPA, Branch, Semester)
- Extracurricular activities (Internships, Projects, Certifications)
- Technical skills management
- Profile picture avatar uploads
- Contact details and social profiles

### 3. **Machine Learning Predictions**
- **Placement Probability**: Classification model predicting placement chances (0-100%)
- **Salary Prediction**: Regression model estimating expected salary package
- **Risk Assessment**: Categorizes students into Low/Medium/High risk groups

### 4. **Unified Result Dashboard**
- Single comprehensive view showing:
  - Placement probability with visual gauge
  - Risk level indicator
  - Expected salary prediction
  - Skill gap analysis
  - Personalized recommendations
  - Resume upload option

### 5. **Skill Gap Analysis**
- Identifies missing important skills based on branch
- Compares student profile against industry requirements
- Provides actionable recommendations
- Priority-based improvement suggestions

### 6. **What-If Simulation**
- Interactive tool to test improvement scenarios
- Modify internships, projects, certifications
- Real-time probability recalculation
- Compare before/after predictions

### 7. **Intelligent Resume Parsing (AI & Fuzzy Logic)**
Unlike standard parsers that rely on strict exact-matching regex, this platform utilizes an advanced **Fuzzy-Logic NLP engine** powered by `thefuzz` (based on Levenshtein distance). 
- **Real-World Error Tolerance:** Automatically detects and corrects misspellings or OCR anomalies in resumes. For example, if a student's resume contains typos like `"Jvascript"`, `"Node js"`, or `"Tensroflow"`, the engine intelligently maps them to the correct master skills (`JavaScript`, `Node.js`, `TensorFlow`).
- **Dynamic Categorization:** Extracts skills and automatically categorizes them into distinct buckets (e.g., Cloud & DevOps, Data Science) to drive the skill-gap analyzer.
- **Auto-Profile Synchronization:** Seamlessly updates the student's internal profile metrics directly from the PDF data.

### 8. **Enterprise-Grade Engineering Standards**
This project transcends academic requirements by implementing strict industry standards:
- 🐳 **Docker Containerization**: The entire application stack is containerized using a custom `Dockerfile` and `docker-compose.yml`. This guarantees perfect environment parity across dev and production, allowing one-click deployments to cloud providers (AWS/GCP).
- 🧪 **Automated Testing Suite**: Implements a robust `pytest` suite ensuring high code reliability. The tests rigorously validate the core Machine Learning heuristics, fallback mechanisms, and the NLP parsing engine, ensuring continuous integration (CI) readiness.
- 🔒 **Cybersecurity Hardening**: Fully abandons hardcoded credentials by employing a secure `.env` variable architecture via `python-dotenv`. This secures database URIs, Flask session keys, and admin credentials from source control leaks.

### 9. **Analytics Dashboard**
- Prediction history visualization
- CGPA vs Placement correlation charts
- Internship impact analysis
- Branch-wise placement statistics
- Interactive Chart.js visualizations

### 10. **Admin Panel**
- View all registered students
- System-wide statistics
- Branch-wise performance analysis
- Recent predictions monitoring

### 11. **PDF Report Generation**
- Comprehensive downloadable reports
- Includes predictions, analysis, and recommendations
- Professional formatting using ReportLab

---

## 🛠️ Technology Stack

### **Frontend**
- HTML5
- CSS3
- Bootstrap 5
- JavaScript (ES6+)
- Chart.js

### **Backend**
- Python 3.12+
- Flask 2.3
- Jinja2 Templates
- Docker & Docker Compose
- PyTest (Automated Testing)

### **Database**
- MySQL 8.0+

### **Machine Learning**
- scikit-learn
- pandas
- numpy
- joblib

### **Libraries**
- PyPDF2 (Resume parsing)
- thefuzz & python-Levenshtein (Fuzzy NLP)
- python-dotenv (Security)
- reportlab (PDF generation)
- Flask-MySQLdb (Database connector)
- Werkzeug (Security)

---

## 📁 Project Structure

```
placement-portal/
│
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose orchestration
├── .env.example                # Security environment variables template
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── database_schema.sql         # MySQL database schema
├── run.bat                     # Windows 1-click startup script
├── run.ps1                     # PowerShell startup script
│
├── tests/                      # Automated PyTest suite
│   ├── conftest.py
│   ├── test_ml_utils.py
│   └── test_resume_parser.py
│
├── models/                     # Database models
│   ├── __init__.py
│   ├── database.py            # Database connection
│   ├── user.py                # User model
│   ├── student.py             # Student profile model
│   ├── prediction.py          # Prediction model
│   └── resume.py              # Resume & skill gap models
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration
│   ├── dashboard.html         # Student dashboard
│   ├── predict.html           # Prediction form
│   ├── results.html           # Unified result panel
│   ├── profile.html           # Profile management
│   ├── upload_resume.html     # Resume upload
│   ├── analytics.html         # Analytics dashboard
│   └── admin_dashboard.html   # Admin panel
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS
│   ├── js/
│   │   └── main.js            # Custom JavaScript
│   └── uploads/               # User uploads
│
├── ml_utils.py                # ML prediction utilities
├── resume_parser.py           # Resume parsing logic
├── pdf_generator.py           # PDF report generation
├── skill_analyzer.py          # Skill gap analysis
│
├── placement_model.pkl        # Trained placement model
├── salary_model.pkl           # Trained salary model
│
├── README.md                  # This file
├── SETUP_GUIDE.md            # Setup instructions
└── VIVA_GUIDE.md             # Viva preparation guide
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip package manager

### Installation

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed manual installation instructions.

**Method 1: Docker (Easiest)**
```bash
docker compose up --build
```

**Method 2: One-Click Windows Script**
Simply double-click the `run.bat` file in the root directory!

**Method 3: Manual Setup**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup Security
copy .env.example .env

# 3. Setup MySQL database
mysql -u root -p < database_schema.sql

# 4. Generate ML models
python generate_models.py

# 5. Run automated tests
pytest tests/ -v

# 6. Run the application
python app.py
```

Access at: `http://localhost:5000`

---

## 📊 Features in Detail

### Machine Learning Models

#### Placement Prediction Model
- **Type**: Random Forest Classifier
- **Features**: CGPA, Branch, Internships, Projects, Certifications, Skills
- **Output**: Probability (0-100%) and Risk Level (Low/Medium/High)

#### Salary Prediction Model
- **Type**: Random Forest Regressor
- **Features**: CGPA, Branch, Internships, Placement Probability
- **Output**: Expected salary in LPA (Lakhs Per Annum)

### Database Schema

**7 Main Tables:**
1. `users` - Authentication
2. `student_profiles` - Student data
3. `predictions` - ML prediction history
4. `resume_data` - Uploaded resumes
5. `skill_gaps` - Skill gap analyses
6. `simulations` - What-if simulations
7. `admin_stats` - Cached statistics

---

## 👤 User Roles

### Student
- Register and manage profile
- Get placement predictions
- Analyze skill gaps
- Run simulations
- Upload resume
- View analytics
- Download reports

### Admin
- View all students
- Monitor predictions
- Access system statistics
- Analyze branch-wise performance

---

## 🎓 For Academic Evaluation

This project demonstrates:
- Full-stack web development
- Machine Learning integration
- Database design and normalization
- RESTful API design
- User authentication and security
- Data visualization
- PDF generation
- File upload handling
- AJAX/Fetch API usage
- Responsive design

---

## 📄 License

This is an educational project created for final year engineering evaluation.

---

## 👨‍💻 Support

For questions regarding setup or implementation:
- Check [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Review [VIVA_GUIDE.md](VIVA_GUIDE.md) for technical explanations

---

## 🙏 Acknowledgments

- Bootstrap for UI framework
- Chart.js for visualizations
- scikit-learn for ML models
- Flask framework
- MySQL database

---

**Project Year**: 2026  
**Category**: Final Year Engineering Project  
**Domain**: Machine Learning, Web Development, Career Guidance
