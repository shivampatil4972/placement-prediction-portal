"""
User Model - Handles user authentication and management
"""

from werkzeug.security import generate_password_hash, check_password_hash
from models.database import execute_query
from datetime import datetime

class User:
    """User model for authentication"""
    
    @staticmethod
    def create_user(email, password, full_name, user_type='student'):
        """Create a new user"""
        password_hash = generate_password_hash(password)
        
        query = """
            INSERT INTO users (email, password_hash, full_name, user_type)
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            user_id = execute_query(
                query, 
                (email, password_hash, full_name, user_type),
                commit=True
            )
            return user_id
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        return execute_query(query, (email,), fetch_one=True)
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        return execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def verify_password(email, password):
        """Verify user password"""
        user = User.get_by_email(email)
        
        if user and check_password_hash(user['password_hash'], password):
            # Update last login
            query = "UPDATE users SET last_login = %s WHERE id = %s"
            execute_query(query, (datetime.now(), user['id']), commit=True)
            return user
        
        return None
    
    @staticmethod
    def email_exists(email):
        """Check if email already exists"""
        user = User.get_by_email(email)
        return user is not None
    
    @staticmethod
    def update_password(user_id, new_password):
        """Update user password"""
        password_hash = generate_password_hash(new_password)
        query = "UPDATE users SET password_hash = %s WHERE id = %s"
        
        try:
            execute_query(query, (password_hash, user_id), commit=True)
            return True
        except:
            return False
    
    @staticmethod
    def get_all_students():
        """Get all student users"""
        query = """
            SELECT u.*, sp.branch, sp.cgpa, sp.enrollment_number
            FROM users u
            LEFT JOIN student_profiles sp ON u.id = sp.user_id
            WHERE u.user_type = 'student'
            ORDER BY u.created_at DESC
        """
        return execute_query(query, fetch_all=True)
    
    @staticmethod
    def get_total_users(user_type=None):
        """Get total user count"""
        if user_type:
            query = "SELECT COUNT(*) as count FROM users WHERE user_type = %s"
            result = execute_query(query, (user_type,), fetch_one=True)
        else:
            query = "SELECT COUNT(*) as count FROM users"
            result = execute_query(query, fetch_one=True)
        
        return result['count'] if result else 0
