"""
Student Profile Model - Handles student profile data
"""

from models.database import execute_query

class StudentProfile:
    """Student profile model"""
    
    @staticmethod
    def create_profile(user_id, branch, cgpa, placement_target='',
                      internship_count=0, project_count=0, certification_count=0,
                      skills=''):
        """Create a new student profile"""
        
        query = """
            INSERT INTO student_profiles 
            (user_id, branch, cgpa, internship_count, 
             project_count, certification_count, skills, placement_target)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        try:
            profile_id = execute_query(
                query,
                (user_id, branch, cgpa, internship_count,
                 project_count, certification_count, skills, placement_target),
                commit=True
            )
            return profile_id
        except Exception as e:
            print(f"Error creating profile: {str(e)}")
            return None
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get student profile by user ID"""
        query = "SELECT * FROM student_profiles WHERE user_id = %s"
        return execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def update_profile(user_id, **kwargs):
        """Update student profile"""
        # Build dynamic update query
        allowed_fields = [
            'branch', 'cgpa', 'internship_count', 'project_count', 
            'certification_count', 'skills', 'placement_target'
        ]
        
        update_fields = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                update_fields.append(f"{field} = %s")
                values.append(value)
        
        if not update_fields:
            return False
        
        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        values.append(user_id)
        query = f"UPDATE student_profiles SET {', '.join(update_fields)} WHERE user_id = %s"
        
        try:
            execute_query(query, tuple(values), commit=True)
            return True
        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            return False
    
    @staticmethod
    def get_skills_list(user_id):
        """Get student skills as a list"""
        profile = StudentProfile.get_by_user_id(user_id)
        if profile and profile['skills']:
            return [skill.strip() for skill in profile['skills'].split(',')]
        return []
    
    @staticmethod
    def add_skills(user_id, new_skills):
        """Add new skills to student profile"""
        current_skills = StudentProfile.get_skills_list(user_id)
        
        # Convert new_skills to list if it's a string
        if isinstance(new_skills, str):
            new_skills = [s.strip() for s in new_skills.split(',')]
        
        # Merge and deduplicate
        all_skills = list(set(current_skills + new_skills))
        skills_str = ', '.join(all_skills)
        
        return StudentProfile.update_profile(user_id, skills=skills_str)
    
    @staticmethod
    def profile_exists(user_id):
        """Check if profile exists for user"""
        profile = StudentProfile.get_by_user_id(user_id)
        return profile is not None
    
    @staticmethod
    def get_all_branches():
        """Get all unique branches"""
        query = "SELECT DISTINCT branch FROM student_profiles ORDER BY branch"
        results = execute_query(query, fetch_all=True)
        return [r['branch'] for r in results] if results else []
    
    @staticmethod
    def get_branch_statistics():
        """Get statistics grouped by branch"""
        query = """
            SELECT 
                branch,
                COUNT(*) as student_count,
                AVG(cgpa) as avg_cgpa,
                AVG(internship_count) as avg_internships,
                AVG(project_count) as avg_projects
            FROM student_profiles
            GROUP BY branch
        """
        return execute_query(query, fetch_all=True)
