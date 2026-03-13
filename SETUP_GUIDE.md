# 📚 Setup Guide - Placement Portal

Complete step-by-step guide to set up the Student Placement Prediction & Strategy Portal on your local machine.

---

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Software Installation](#software-installation)
3. [Database Setup](#database-setup)
4. [Project Configuration](#project-configuration)
5. [Generating ML Models](#generating-ml-models)
6. [Running the Application](#running-the-application)
7. [Default Credentials](#default-credentials)
8. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS, or Linux
- **RAM**: 4GB (8GB recommended)
- **Storage**: 500MB free space
- **Internet**: Required for initial setup

### Required Software
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip (Python package manager)
- Git (optional)
- Web browser (Chrome, Firefox, Edge)

---

## 🔧 Software Installation

### Step 1: Install Python

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Complete installation

**Verify installation:**
```bash
python --version
pip --version
```

#### macOS
```bash
# Using Homebrew
brew install python@3.12
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 2: Install MySQL

#### Windows
1. Download MySQL Installer from [mysql.com](https://dev.mysql.com/downloads/installer/)
2. Run installer and choose "Developer Default"
3. Set root password (remember this!)
4. Complete installation

#### macOS
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

#### Linux
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**Verify MySQL:**
```bash
mysql --version
```

### Step 3: Install Git (Optional)
- Windows: [git-scm.com](https://git-scm.com/)
- macOS: `brew install git`
- Linux: `sudo apt install git`

---

## 📦 Project Setup

### Step 1: Extract/Clone Project

**Option A: Extract ZIP**
1. Extract the project ZIP file
2. Navigate to the folder:
```bash
cd "PLACEMENT PORTAL"
```

**Option B: Clone (if available)**
```bash
git clone <repository-url>
cd placement-portal
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**This installs:**
- Flask (Web framework)
- Flask-MySQLdb (Database connector)
- scikit-learn (Machine Learning)
- pandas, numpy (Data processing)
- PyPDF2 (PDF parsing)
- reportlab (PDF generation)
- And more...

**Wait for installation to complete** (may take 2-5 minutes)

---

## 🗄️ Database Setup

### Step 1: Start MySQL Server

**Windows:**
- MySQL should start automatically
- Or: Start from Services

**macOS/Linux:**
```bash
# macOS
brew services start mysql

# Linux
sudo systemctl start mysql
```

### Step 2: Login to MySQL

```bash
mysql -u root -p
```
Enter your root password when prompted.

### Step 3: Create Database

**Option A: Using SQL file (Recommended)**

Exit MySQL and run:
```bash
mysql -u root -p < database_schema.sql
```

**Option B: Manual creation**

In MySQL prompt:
```sql
SOURCE database_schema.sql;
```

### Step 4: Verify Database

```sql
USE placement_portal;
SHOW TABLES;
```

You should see 7 tables:
- users
- student_profiles
- predictions
- resume_data
- skill_gaps
- simulations
- admin_stats

Exit MySQL:
```sql
EXIT;
```

---

## ⚙️ Project Configuration

### Step 1: Edit config.py

Open `config.py` and update MySQL credentials:

```python
# MySQL Database Configuration
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'          # Your MySQL username
MYSQL_PASSWORD = 'your_password'  # Your MySQL password
MYSQL_DB = 'placement_portal'
```

### Step 2: Update Secret Key (Important for Production)

```python
SECRET_KEY = 'your-secret-key-here'  # Change this!
```

Generate a secure key:
```python
import secrets
print(secrets.token_hex(16))
```

### Step 3: Create Upload Directory

The directory should already exist, but verify:
```bash
# Windows
dir static\uploads

# macOS/Linux
ls -la static/uploads
```

---

## 🤖 Generating ML Models

### Step 1: Run Model Generator

```bash
python generate_models.py
```

**What this does:**
- Creates synthetic training data (1000 samples)
- Trains a Random Forest Classifier for placement prediction
- Trains a Random Forest Regressor for salary prediction
- Saves models as `.pkl` files
- Tests models with sample predictions

**Expected output:**
```
Placement model saved as 'placement_model.pkl'
Salary model saved as 'salary_model.pkl'
✓ MODEL GENERATION COMPLETE!
```

**Verify files created:**
```bash
# Windows
dir *.pkl

# macOS/Linux
ls -l *.pkl
```

You should see:
- `placement_model.pkl`
- `salary_model.pkl`

### Alternative: Use Pre-trained Models

If models are already provided, skip this step.

---

## 🚀 Running the Application

### Step 1: Start Flask Server

```bash
python app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Step 2: Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

or
```
http://127.0.0.1:5000
```

### Step 3: Stop the Server

Press `Ctrl+C` in the terminal.

---

## 🔐 Default Credentials

### Admin Account

After running `database_schema.sql`, update admin password:

**Option 1: Using Python**
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash('admin123'))
```

Copy the hash and update in MySQL:
```sql
UPDATE users 
SET password_hash = 'your-generated-hash' 
WHERE email = 'admin@placement.com';
```

**Default Admin Login:**
- Email: `admin@placement.com`
- Password: `admin123` (after updating hash)

### Student Account

Create via registration page or insert manually:
```sql
INSERT INTO users (email, password_hash, full_name, user_type)
VALUES ('student@test.com', 'hash-here', 'Test Student', 'student');
```

---

## 🔧 Troubleshooting

### Issue 1: MySQL Connection Failed

**Error:** `Can't connect to MySQL server`

**Solution:**
```bash
# Check if MySQL is running
# Windows
sc query MySQL80

# macOS
brew services list

# Linux
sudo systemctl status mysql

# Start MySQL if stopped
sudo systemctl start mysql
```

### Issue 2: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Run on different port
python app.py --port 5001

# Or kill the process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <process-id> /F

# macOS/Linux
lsof -ti:5000 | xargs kill
```

### Issue 4: Database Tables Not Created

**Solution:**
```bash
# Re-run schema
mysql -u root -p placement_portal < database_schema.sql
```

### Issue 5: Permission Denied on Uploads

**Solution:**
```bash
# Windows (Run as Administrator)
icacls "static\uploads" /grant Everyone:F

# macOS/Linux
chmod 777 static/uploads
```

### Issue 6: ML Models Not Found

**Error:** `FileNotFoundError: placement_model.pkl`

**Solution:**
```bash
# Regenerate models
python generate_models.py

# Verify files exist
ls -l *.pkl
```

### Issue 7: PDF Generation Fails

**Solution:**
```bash
# Install reportlab
pip install reportlab

# Check file permissions
chmod 777 static/uploads
```

---

## 📱 Testing the Application

### 1. Register a New Student
- Go to `/register`
- Fill in details
- Submit

### 2. Make a Prediction
- Login
- Go to "Predict" page
- Enter details
- View results

### 3. Upload Resume
- Go to "Resume" tab
- Upload a PDF resume
- View extracted skills

### 4. Admin Panel
- Login as admin
- View dashboard
- Check statistics

---

## 🔄 Updating the Project

### Pull Latest Changes
```bash
git pull origin main
```

### Update Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Backup Database
```bash
mysqldump -u root -p placement_portal > backup.sql
```

---

## 🌐 Deployment (Optional)

### For Production Deployment:

1. **Disable Debug Mode**
   ```python
   # In app.py
   app.run(debug=False)
   ```

2. **Use Production Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```

3. **Setup HTTPS**
   - Use SSL certificates
   - Configure reverse proxy (Nginx/Apache)

4. **Environment Variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   ```

---

## ✅ Setup Verification Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL 8.0+ installed and running
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database created and tables exist
- [ ] `config.py` updated with MySQL credentials
- [ ] ML models generated (`.pkl` files exist)
- [ ] Flask app runs without errors
- [ ] Can access `http://localhost:5000`
- [ ] Can register a new student
- [ ] Can make a prediction
- [ ] Can upload a resume

---

## 📞 Getting Help

If you encounter issues not covered here:

1. Check error messages carefully
2. Verify all steps were completed
3. Ensure all services are running
4. Check file permissions
5. Review the README.md
6. Consult VIVA_GUIDE.md for technical details

---

**Setup Complete! 🎉**

You're now ready to use the Placement Portal!
