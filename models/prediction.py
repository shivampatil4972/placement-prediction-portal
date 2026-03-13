"""
Prediction Model - Handles ML prediction history
"""

from models.database import execute_query
from datetime import datetime, timedelta

class Prediction:
    """Prediction model for storing ML results"""
    
    @staticmethod
    def save_prediction(user_id, placement_probability, predicted_salary, risk_level,
                       cgpa, branch, internship_count, project_count, 
                       certification_count, skill_count):
        """Save a prediction result"""
        
        query = """
            INSERT INTO predictions 
            (user_id, placement_probability, expected_salary, risk_level, cgpa,
             branch, internship_count, project_count, certification_count, skill_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            prediction_id = execute_query(
                query,
                (user_id, placement_probability, predicted_salary, risk_level, cgpa,
                 branch, internship_count, project_count, certification_count, skill_count),
                commit=True
            )
            return prediction_id
        except Exception as e:
            print(f"Error saving prediction: {str(e)}")
            return None
    
    @staticmethod
    def get_user_predictions(user_id, limit=10):
        """Get prediction history for a user"""
        query = """
            SELECT * FROM predictions 
            WHERE user_id = %s 
            ORDER BY prediction_date DESC 
            LIMIT %s
        """
        return execute_query(query, (user_id, limit), fetch_all=True)
    
    @staticmethod
    def get_latest_prediction(user_id):
        """Get most recent prediction for user"""
        query = """
            SELECT * FROM predictions 
            WHERE user_id = %s 
            ORDER BY prediction_date DESC 
            LIMIT 1
        """
        return execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def get_all_predictions(limit=100):
        """Get all recent predictions"""
        query = """
            SELECT p.*, u.full_name, u.email 
            FROM predictions p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.prediction_date DESC
            LIMIT %s
        """
        return execute_query(query, (limit,), fetch_all=True)
    
    @staticmethod
    def get_average_probability():
        """Get average placement probability across all students"""
        query = """
            SELECT AVG(placement_probability) as avg_probability
            FROM (
                SELECT user_id, MAX(placement_probability) as placement_probability
                FROM predictions
                GROUP BY user_id
            ) as latest_predictions
        """
        result = execute_query(query, fetch_one=True)
        return round(result['avg_probability'], 2) if result and result['avg_probability'] else 0
    
    @staticmethod
    def get_prediction_trends(user_id):
        """Get prediction trends for charts"""
        query = """
            SELECT 
                DATE(prediction_date) as date,
                placement_probability,
                expected_salary
            FROM predictions
            WHERE user_id = %s
            ORDER BY prediction_date ASC
        """
        return execute_query(query, (user_id,), fetch_all=True)
    
    @staticmethod
    def get_cgpa_vs_placement_data():
        """Get CGPA vs placement probability data for charts"""
        query = """
            SELECT 
                ROUND(cgpa, 1) as cgpa_range,
                AVG(placement_probability) as avg_probability,
                COUNT(*) as count
            FROM predictions
            GROUP BY ROUND(cgpa, 1)
            ORDER BY cgpa_range
        """
        return execute_query(query, fetch_all=True)
    
    @staticmethod
    def get_internship_impact_data():
        """Get internship count vs placement probability"""
        query = """
            SELECT 
                internship_count,
                AVG(placement_probability) as avg_probability,
                COUNT(*) as count
            FROM predictions
            GROUP BY internship_count
            ORDER BY internship_count
        """
        return execute_query(query, fetch_all=True)
    
    @staticmethod
    def get_branch_placement_data():
        """Get branch-wise placement statistics"""
        query = """
            SELECT 
                branch,
                AVG(placement_probability) as avg_probability,
                COUNT(DISTINCT user_id) as student_count
            FROM predictions
            GROUP BY branch
            ORDER BY avg_probability DESC
        """
        return execute_query(query, fetch_all=True)
