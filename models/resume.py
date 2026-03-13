"""
Resume Model - Handles resume upload and parsing
"""

from models.database import execute_query

class Resume:
    """Resume model for file uploads and skill extraction"""
    
    @staticmethod
    def save_resume(user_id, file_name, file_path, extracted_skills, extracted_text):
        """Save resume data"""
        
        query = """
            INSERT INTO resume_data 
            (user_id, file_name, file_path, extracted_skills, extracted_text)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            resume_id = execute_query(
                query,
                (user_id, file_name, file_path, extracted_skills, extracted_text),
                commit=True
            )
            return resume_id
        except Exception as e:
            print(f"Error saving resume: {str(e)}")
            return None
    
    @staticmethod
    def get_user_resumes(user_id):
        """Get all resumes for a user"""
        query = """
            SELECT * FROM resume_data 
            WHERE user_id = %s 
            ORDER BY upload_date DESC
        """
        return execute_query(query, (user_id,), fetch_all=True)
    
    @staticmethod
    def get_latest_resume(user_id):
        """Get most recent resume for user"""
        query = """
            SELECT * FROM resume_data 
            WHERE user_id = %s 
            ORDER BY upload_date DESC 
            LIMIT 1
        """
        return execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def delete_resume(resume_id, user_id):
        """Delete a resume"""
        query = "DELETE FROM resume_data WHERE id = %s AND user_id = %s"
        try:
            execute_query(query, (resume_id, user_id), commit=True)
            return True
        except:
            return False


class SkillGap:
    """Skill gap analysis model"""
    
    @staticmethod
    def save_analysis(user_id, missing_skills, recommended_actions, priority='Medium'):
        """Save skill gap analysis"""
        
        # Convert lists to strings if needed
        if isinstance(missing_skills, list):
            missing_skills = ', '.join(missing_skills)
        if isinstance(recommended_actions, list):
            recommended_actions = '\n'.join(recommended_actions)
        
        query = """
            INSERT INTO skill_gaps 
            (user_id, missing_skills, recommended_actions, priority)
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            gap_id = execute_query(
                query,
                (user_id, missing_skills, recommended_actions, priority),
                commit=True
            )
            return gap_id
        except Exception as e:
            print(f"Error saving skill gap: {str(e)}")
            return None
    
    @staticmethod
    def get_latest_analysis(user_id):
        """Get most recent skill gap analysis"""
        query = """
            SELECT * FROM skill_gaps 
            WHERE user_id = %s 
            ORDER BY analysis_date DESC 
            LIMIT 1
        """
        return execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def get_user_analyses(user_id, limit=5):
        """Get skill gap history for user"""
        query = """
            SELECT * FROM skill_gaps 
            WHERE user_id = %s 
            ORDER BY analysis_date DESC 
            LIMIT %s
        """
        return execute_query(query, (user_id, limit), fetch_all=True)


class Simulation:
    """What-if simulation model"""
    
    @staticmethod
    def save_simulation(user_id, original_probability, simulated_probability, changes_made):
        """Save a what-if simulation"""
        
        # Convert dict to string if needed
        if isinstance(changes_made, dict):
            changes_made = str(changes_made)
        
        query = """
            INSERT INTO simulations 
            (user_id, original_probability, simulated_probability, changes_made)
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            sim_id = execute_query(
                query,
                (user_id, original_probability, simulated_probability, changes_made),
                commit=True
            )
            return sim_id
        except Exception as e:
            print(f"Error saving simulation: {str(e)}")
            return None
    
    @staticmethod
    def get_user_simulations(user_id, limit=10):
        """Get simulation history for user"""
        query = """
            SELECT * FROM simulations 
            WHERE user_id = %s 
            ORDER BY simulation_date DESC 
            LIMIT %s
        """
        return execute_query(query, (user_id, limit), fetch_all=True)
