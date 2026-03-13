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

### 7. **Resume Upload & Parsing**
- PDF resume upload
- Automatic skill extraction using NLP
- Skill matching with keyword database
- Option to auto-update profile

### 8. **Analytics Dashboard**
- Prediction history visualization
- CGPA vs Placement correlation charts
- Internship impact analysis
- Branch-wise placement statistics
- Interactive Chart.js visualizations

### 9. **Admin Panel**
- View all registered students
- System-wide statistics
- Branch-wise performance analysis
- Recent predictions monitoring

### 10. **PDF Report Generation**
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
- Python 3.8+
- Flask 2.3
- Jinja2 Templates

### **Database**
- MySQL 8.0+

### **Machine Learning**
- scikit-learn
- pandas
- numpy
- joblib

### **Libraries**
- PyPDF2 (Resume parsing)
- reportlab (PDF generation)
- Flask-MySQLdb (Database connector)
- Werkzeug (Security)

---

## 📁 Project Structure

```
placement-portal/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── database_schema.sql         # MySQL database schema
├── generate_models.py          # ML model generator script
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

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed installation instructions.

**Quick Setup:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup MySQL database
mysql -u root -p < database_schema.sql

# 3. Update config.py with your MySQL credentials

# 4. Generate ML models
python generate_models.py

# 5. Run the application
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
