"""
Main Flask Application
Student Placement Prediction & Strategy Portal
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json

# Import configurations
from config import Config

# Import models
from models import init_db, User, StudentProfile, Prediction, Resume, SkillGap, Simulation

# Import utilities
from ml_utils import ml_predictor
from resume_parser import resume_parser
from pdf_generator import report_generator
from skill_analyzer import skill_analyzer

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ============================================
# HELPER FUNCTIONS
# ============================================

def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('user_type') != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    
    return decorated_function


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ============================================
# AUTHENTICATION ROUTES
# ============================================

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        if session.get('user_type') == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration"""
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        branch = request.form.get('branch')
        cgpa = float(request.form.get('cgpa', 0))
        
        # Validation
        if not all([email, password, full_name, branch]):
            flash('All required fields must be filled.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return redirect(url_for('register'))
        
        if cgpa < 0 or cgpa > 10:
            flash('CGPA must be between 0 and 10.', 'danger')
            return redirect(url_for('register'))
        
        # Check if email already exists
        if User.email_exists(email):
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('login'))
        
        # Create user
        user_id = User.create_user(email, password, full_name, 'student')
        
        if user_id:
            # Create student profile
            profile_id = StudentProfile.create_profile(
                user_id=user_id,
                branch=branch,
                cgpa=cgpa
            )
            
            if profile_id:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error creating profile. Please try again.', 'danger')
        else:
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('login'))
        
        # Verify credentials
        user = User.verify_password(email, password)
        
        if user:
            # Set session
            session['user_id'] = user['id']
            session['user_type'] = user['user_type']
            session['full_name'] = user['full_name']
            session['email'] = user['email']
            
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            
            if user['user_type'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


# ============================================
# STUDENT DASHBOARD & PROFILE
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Student dashboard"""
    user_id = session['user_id']
    
    # Get user and profile data
    user = User.get_by_id(user_id)
    profile = StudentProfile.get_by_user_id(user_id)
    
    # Create default profile if doesn't exist
    if not profile:
        StudentProfile.create_profile(
            user_id=user_id,
            branch='Computer Science',
            cgpa=0.0
        )
        profile = StudentProfile.get_by_user_id(user_id)
    
    # Get latest prediction
    latest_prediction = Prediction.get_latest_prediction(user_id)
    
    # Get prediction history
    prediction_history = Prediction.get_user_predictions(user_id, limit=5)
    
    # Get latest skill gap analysis
    skill_gap = SkillGap.get_latest_analysis(user_id)
    
    return render_template('dashboard.html',
                         user=user,
                         profile=profile,
                         latest_prediction=latest_prediction,
                         prediction_history=prediction_history,
                         skill_gap=skill_gap)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and edit student profile"""
    user_id = session['user_id']
    
    if request.method == 'POST':
        # Update profile
        update_data = {
            'branch': request.form.get('branch'),
            'cgpa': float(request.form.get('cgpa')),
            'internship_count': int(request.form.get('internship_count', 0)),
            'project_count': int(request.form.get('project_count', 0)),
            'certification_count': int(request.form.get('certification_count', 0)),
            'skills': request.form.get('skills', ''),
            'placement_target': request.form.get('placement_target', '')
        }
        
        if StudentProfile.update_profile(user_id, **update_data):
            flash('Profile updated successfully!', 'success')
        else:
            flash('Error updating profile.', 'danger')
        
        return redirect(url_for('profile'))
    
    # GET request
    user = User.get_by_id(user_id)
    profile_data = StudentProfile.get_by_user_id(user_id)
    
    # Create default profile if doesn't exist
    if not profile_data:
        StudentProfile.create_profile(
            user_id=user_id,
            branch='Computer Science',
            cgpa=0.0
        )
        profile_data = StudentProfile.get_by_user_id(user_id)
    
    return render_template('profile.html', user=user, profile=profile_data)


# ============================================
# ML PREDICTION ROUTES
# ============================================

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    """Placement prediction"""
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    profile = StudentProfile.get_by_user_id(user_id)
    
    if request.method == 'POST' or request.is_json:
        # Get data from form or JSON (for AJAX)
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        # Extract parameters - handle missing profile gracefully
        cgpa = float(data.get('cgpa', profile['cgpa'] if profile else 0))
        branch = data.get('branch', profile['branch'] if profile else 'Computer Science')
        internship_count = int(data.get('internship_count', profile['internship_count'] if profile else 0))
        project_count = int(data.get('project_count', profile['project_count'] if profile else 0))
        certification_count = int(data.get('certification_count', profile['certification_count'] if profile else 0))
        skills = data.get('skills', profile['skills'] if profile else '')
        
        # Count skills
        skill_list = [s.strip() for s in skills.split(',') if s.strip()]
        skill_count = len(skill_list)
        
        # ML Prediction
        placement_prob = ml_predictor.predict_placement(
            cgpa, branch, internship_count, project_count, 
            certification_count, skill_count
        )
        
        predicted_salary = ml_predictor.predict_salary(
            cgpa, branch, internship_count, placement_prob
        )
        
        risk_level = ml_predictor.get_risk_level(placement_prob)
        
        # Skill gap analysis
        skill_gap_analysis = skill_analyzer.analyze(
            {
                'branch': branch,
                'skills': skills,
                'cgpa': cgpa,
                'internship_count': internship_count,
                'project_count': project_count,
                'certification_count': certification_count
            },
            placement_prob
        )
        
        # Save prediction to database
        prediction_id = Prediction.save_prediction(
            user_id=user_id,
            placement_probability=placement_prob,
            predicted_salary=predicted_salary,
            risk_level=risk_level,
            cgpa=cgpa,
            branch=branch,
            internship_count=internship_count,
            project_count=project_count,
            certification_count=certification_count,
            skill_count=skill_count
        )
        
        # Save skill gap analysis
        SkillGap.save_analysis(
            user_id=user_id,
            missing_skills=skill_gap_analysis['missing_skills_str'],
            recommended_actions='\n'.join(skill_gap_analysis['recommendations']),
            priority=skill_gap_analysis['priority']
        )
        
        # If AJAX request, return JSON
        if request.is_json:
            return jsonify({
                'success': True,
                'placement_probability': placement_prob,
                'predicted_salary': predicted_salary,
                'risk_level': risk_level,
                'skill_gap': skill_gap_analysis
            })
        
        # Redirect to results page
        return redirect(url_for('results'))
    
    return render_template('predict.html', user=user, profile=profile)


@app.route('/results')
@login_required
def results():
    """Show prediction results"""
    user_id = session['user_id']
    
    # Get latest prediction
    prediction = Prediction.get_latest_prediction(user_id)
    
    if not prediction:
        flash('No prediction found. Please make a prediction first.', 'warning')
        return redirect(url_for('predict'))
    
    # Get skill gap analysis
    skill_gap = SkillGap.get_latest_analysis(user_id)
    
    # Get profile for additional info
    profile = StudentProfile.get_by_user_id(user_id)
    user = User.get_by_id(user_id)
    
    return render_template('results.html',
                         prediction=prediction,
                         skill_gap=skill_gap,
                         profile=profile,
                         user=user)


# ============================================
# WHAT-IF SIMULATION
# ============================================

@app.route('/simulate', methods=['POST'])
@login_required
def simulate():
    """What-if simulation (AJAX endpoint)"""
    user_id = session['user_id']
    profile = StudentProfile.get_by_user_id(user_id)
    
    data = request.get_json()
    
    # Get modified parameters - handle missing profile gracefully
    cgpa = float(data.get('cgpa', profile['cgpa'] if profile else 0))
    branch = data.get('branch', profile['branch'] if profile else 'Computer Science')
    internship_count = int(data.get('internship_count', profile['internship_count'] if profile else 0))
    project_count = int(data.get('project_count', profile['project_count'] if profile else 0))
    certification_count = int(data.get('certification_count', profile['certification_count'] if profile else 0))
    skills = data.get('skills', profile['skills'] if profile else '')
    
    skill_count = len([s.strip() for s in skills.split(',') if s.strip()])
    
    # Get original probability
    original_prob = data.get('original_probability', 0)
    
    # Calculate new probability
    new_prob = ml_predictor.predict_placement(
        cgpa, branch, internship_count, project_count, 
        certification_count, skill_count
    )
    
    new_salary = ml_predictor.predict_salary(cgpa, branch, internship_count, new_prob)
    new_risk = ml_predictor.get_risk_level(new_prob)
    
    # Save simulation
    changes = {
        'internship_count': internship_count,
        'project_count': project_count,
        'certification_count': certification_count,
        'skill_count': skill_count
    }
    
    Simulation.save_simulation(
        user_id=user_id,
        original_probability=original_prob,
        simulated_probability=new_prob,
        changes_made=str(changes)
    )
    
    return jsonify({
        'success': True,
        'new_probability': new_prob,
        'new_salary': new_salary,
        'new_risk': new_risk,
        'improvement': round(new_prob - original_prob, 2)
    })


# ============================================
# RESUME UPLOAD & PARSING
# ============================================

@app.route('/upload_resume', methods=['GET', 'POST'])
@login_required
def upload_resume():
    """Upload and parse resume"""
    user_id = session['user_id']
    
    if request.method == 'POST':
        # Debug: Log what's in the request
        print(f"Files in request: {request.files.keys()}")
        print(f"Form data: {request.form.keys()}")
        
        # Check if file was uploaded
        if 'resume' not in request.files:
            flash('No file part in the request. Please select a file.', 'danger')
            return redirect(request.url)
        
        file = request.files['resume']
        
        if file.filename == '':
            flash('No file selected. Please choose a PDF file.', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Secure filename
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{user_id}_{timestamp}_{filename}"
                
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # Parse resume
                analysis = resume_parser.analyze_resume(filepath)
                
                if analysis:
                    # Save to database
                    extracted_skills_str = ', '.join(analysis['skills'])
                    
                    Resume.save_resume(
                        user_id=user_id,
                        file_name=filename,
                        file_path=filepath,
                        extracted_skills=extracted_skills_str,
                        extracted_text=analysis['text'][:1000]  # Store first 1000 chars
                    )
                    
                    flash(f'Resume uploaded successfully! Found {analysis["skill_count"]} skills.', 'success')
                    
                    # Optionally add skills to profile
                    if request.form.get('add_to_profile') == 'yes':
                        StudentProfile.add_skills(user_id, analysis['skills'])
                        flash('Skills added to your profile!', 'success')
                    
                    return render_template('resume_analysis.html', analysis=analysis)
                else:
                    flash('Error analyzing resume. Please ensure it\'s a valid PDF with text content.', 'danger')
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'danger')
                print(f"Resume upload error: {str(e)}")
        else:
            flash('Only PDF files are allowed. Please upload a .pdf file.', 'danger')
    
    # GET request
    user_resumes = Resume.get_user_resumes(user_id)
    return render_template('upload_resume.html', resumes=user_resumes)


# ============================================
# ANALYTICS & CHARTS
# ============================================

@app.route('/analytics')
@login_required
def analytics():
    """Analytics dashboard with charts"""
    user_id = session['user_id']
    
    # Get prediction trends
    trends = Prediction.get_prediction_trends(user_id)
    
    # Get history
    history = Prediction.get_user_predictions(user_id, limit=10)
    
    # Get simulations
    simulations = Simulation.get_user_simulations(user_id, limit=5)
    
    return render_template('analytics.html',
                         trends=trends,
                         history=history,
                         simulations=simulations)


@app.route('/api/chart-data/<chart_type>')
@login_required
def chart_data(chart_type):
    """API endpoint for chart data"""
    
    if chart_type == 'cgpa_vs_placement':
        data = Prediction.get_cgpa_vs_placement_data()
        return jsonify({
            'labels': [str(d['cgpa_range']) for d in data],
            'values': [float(d['avg_probability']) for d in data]
        })
    
    elif chart_type == 'internship_impact':
        data = Prediction.get_internship_impact_data()
        return jsonify({
            'labels': [f"{d['internship_count']} Internships" for d in data],
            'values': [float(d['avg_probability']) for d in data]
        })
    
    elif chart_type == 'branch_placement':
        data = Prediction.get_branch_placement_data()
        return jsonify({
            'labels': [d['branch'] for d in data],
            'values': [float(d['avg_probability']) for d in data]
        })
    
    elif chart_type == 'user_trends':
        user_id = session['user_id']
        data = Prediction.get_prediction_trends(user_id)
        return jsonify({
            'labels': [str(d['date']) for d in data],
            'probability': [float(d['placement_probability']) for d in data],
            'salary': [float(d['expected_salary']) for d in data]
        })
    
    return jsonify({'error': 'Invalid chart type'}), 400


# ============================================
# ADMIN PANEL
# ============================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    
    # Get statistics
    total_students = User.get_total_users('student')
    avg_probability = Prediction.get_average_probability()
    
    # Get recent predictions
    recent_predictions = Prediction.get_all_predictions(limit=20)
    
    # Get branch statistics
    branch_stats = StudentProfile.get_branch_statistics()
    
    # Get all students
    all_students = User.get_all_students()
    
    return render_template('admin_dashboard.html',
                         total_students=total_students,
                         avg_probability=avg_probability,
                         recent_predictions=recent_predictions,
                         branch_stats=branch_stats,
                         all_students=all_students)


@app.route('/admin/students')
@admin_required
def admin_students():
    """View all students"""
    students = User.get_all_students()
    return render_template('admin_students.html', students=students)


@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    """Admin analytics page"""
    
    # Global analytics data
    cgpa_data = Prediction.get_cgpa_vs_placement_data()
    internship_data = Prediction.get_internship_impact_data()
    branch_data = Prediction.get_branch_placement_data()
    
    return render_template('admin_analytics.html',
                         cgpa_data=cgpa_data,
                         internship_data=internship_data,
                         branch_data=branch_data)


# ============================================
# PDF REPORT GENERATION
# ============================================

@app.route('/download_report')
@login_required
def download_report():
    """Generate and download PDF report"""
    user_id = session['user_id']
    
    # Get user data
    user = User.get_by_id(user_id)
    profile = StudentProfile.get_by_user_id(user_id)
    prediction = Prediction.get_latest_prediction(user_id)
    skill_gap = SkillGap.get_latest_analysis(user_id)
    
    if not prediction:
        flash('No prediction found. Please make a prediction first.', 'warning')
        return redirect(url_for('predict'))
    
    # Prepare data
    prediction_data = {
        'placement_probability': prediction['placement_probability'],
        'predicted_salary': prediction['expected_salary'],
        'risk_level': prediction['risk_level']
    }
    
    skill_gap_data = {
        'missing_skills': skill_gap['missing_skills'] if skill_gap else 'None',
        'priority': skill_gap['priority'] if skill_gap else 'Medium'
    }
    
    # Get suggestions
    if skill_gap:
        suggestions = skill_gap['recommended_actions'].split('\n')
    else:
        suggestions = ['Continue improving your technical skills.']
    
    # Generate PDF
    filename = f"placement_report_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    report_generator.generate_placement_report(
        filename=filepath,
        user_data=user,
        profile_data=profile,
        prediction_data=prediction_data,
        skill_gap_data=skill_gap_data,
        suggestions=suggestions
    )
    
    return send_file(filepath, as_attachment=True, download_name=f"Placement_Report_{user['full_name']}.pdf")


# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500


# ============================================
# RUN APPLICATION
# ============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
