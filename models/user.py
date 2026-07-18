"""
User Model - Handles user authentication and management
"""

from werkzeug.security import generate_password_hash, check_password_hash
from models.database import execute_query
from datetime import datetime, timedelta
import secrets

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
    def update_profile_pic(user_id, filename):
        """Update user profile picture"""
        query = "UPDATE users SET profile_pic = %s WHERE id = %s"
        try:
            execute_query(query, (filename, user_id), commit=True)
            return True
        except Exception as e:
            print(f"Error updating profile pic: {e}")
            return False

    @staticmethod
    def create_password_reset_token(email, expiry_minutes=30):
        """Create password reset token for a user email"""
        user = User.get_by_email(email)
        if not user:
            return None

        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(minutes=expiry_minutes)

        query = """
            UPDATE users
            SET reset_token = %s, reset_token_expires_at = %s
            WHERE id = %s
        """

        try:
            execute_query(query, (token, expires_at.isoformat(), user['id']), commit=True)
            return token
        except Exception as e:
            print(f"Error creating password reset token: {str(e)}")
            return None

    @staticmethod
    def get_by_reset_token(token):
        """Get user by valid reset token"""
        query = "SELECT * FROM users WHERE reset_token = %s"
        user = execute_query(query, (token,), fetch_one=True)

        if not user:
            return None

        expires_at = user.get('reset_token_expires_at')
        if not expires_at:
            return None

        try:
            expiry_dt = datetime.fromisoformat(expires_at)
        except ValueError:
            return None

        if datetime.utcnow() > expiry_dt:
            return None

        return user

    @staticmethod
    def reset_password_with_token(token, new_password):
        """Reset password using reset token"""
        user = User.get_by_reset_token(token)
        if not user:
            return False

        password_hash = generate_password_hash(new_password)
        query = """
            UPDATE users
            SET password_hash = %s,
                reset_token = NULL,
                reset_token_expires_at = NULL
            WHERE id = %s
        """

        try:
            execute_query(query, (password_hash, user['id']), commit=True)
            return True
        except Exception as e:
            print(f"Error resetting password: {str(e)}")
            return False

    @staticmethod
    def clear_reset_token(user_id):
        """Clear reset token values for a user"""
        query = "UPDATE users SET reset_token = NULL, reset_token_expires_at = NULL WHERE id = %s"
        try:
            execute_query(query, (user_id,), commit=True)
            return True
        except Exception as e:
            print(f"Error clearing reset token: {str(e)}")
            return False
    
    @staticmethod
    def get_all_students():
        """Get all student users"""
        query = """
            SELECT u.*, sp.branch, sp.cgpa
            FROM users u
            LEFT JOIN student_profiles sp ON u.id = sp.user_id
            WHERE u.user_type = 'student'
            ORDER BY u.created_at DESC
        """
        return execute_query(query, fetch_all=True)

    @staticmethod
    def get_all_users():
        """Get all users with profile details if available."""
        query = """
            SELECT u.*, sp.branch, sp.cgpa
            FROM users u
            LEFT JOIN student_profiles sp ON u.id = sp.user_id
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

    @staticmethod
    def ensure_admin_exists(email, password, full_name='Admin User'):
        """Ensure a default admin user exists for initial setup."""
        existing = User.get_by_email(email)

        if existing:
            if existing.get('user_type') != 'admin':
                query = "UPDATE users SET user_type = %s WHERE id = %s"
                execute_query(query, ('admin', existing['id']), commit=True)
            return existing['id']

        return User.create_user(email, password, full_name, 'admin')

    @staticmethod
    def set_user_type(user_id, user_type):
        """Update role for a user."""
        query = "UPDATE users SET user_type = %s WHERE id = %s"
        try:
            execute_query(query, (user_type, user_id), commit=True)
            return True
        except Exception as e:
            print(f"Error updating user type: {str(e)}")
            return False

    @staticmethod
    def delete_user(user_id):
        """Delete user account."""
        query = "DELETE FROM users WHERE id = %s"
        try:
            execute_query(query, (user_id,), commit=True)
            return True
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return False
