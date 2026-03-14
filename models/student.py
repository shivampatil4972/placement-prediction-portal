"""
Student Profile Model - Handles student profile data
"""

import re

from models.database import execute_query

class StudentProfile:
    """Student profile model"""

    # Normalize common aliases so resume and manual entries merge cleanly.
    SKILL_ALIASES = {
        'js': 'JavaScript',
        'javascript': 'JavaScript',
        'ts': 'TypeScript',
        'py': 'Python',
        'c sharp': 'C#',
        'c#': 'C#',
        'cpp': 'C++',
        'nodejs': 'Node.js',
        'node js': 'Node.js',
        'reactjs': 'React',
        'react js': 'React',
        'ml': 'Machine Learning',
        'ai': 'AI',
        'nlp': 'NLP',
        'rest': 'REST API',
        'restful api': 'REST API',
        'sql': 'SQL',
        'dsa': 'Data Structures and Algorithms',
        'data structures': 'Data Structures and Algorithms',
        'algorithms': 'Data Structures and Algorithms',
        'github': 'GitHub',
        'git hub': 'GitHub'
    }

    @staticmethod
    def _canonicalize_skill(skill):
        """Convert any skill representation to a clean canonical display form."""
        cleaned = re.sub(r'\s+', ' ', str(skill).strip())
        if not cleaned:
            return ''

        lowered = cleaned.lower()
        if lowered in StudentProfile.SKILL_ALIASES:
            return StudentProfile.SKILL_ALIASES[lowered]

        # Preserve acronyms and known symbols.
        preserved = {
            'sql': 'SQL',
            'api': 'API',
            'oop': 'OOP',
            'ai': 'AI',
            'nlp': 'NLP',
            'c++': 'C++',
            'c#': 'C#',
            'aws': 'AWS',
            'css': 'CSS',
            'html': 'HTML'
        }
        if lowered in preserved:
            return preserved[lowered]

        return cleaned.title()

    @staticmethod
    def _normalize_skills_input(skills_value):
        """Parse comma/newline separated skills into canonical list preserving order."""
        if skills_value is None:
            return []

        if isinstance(skills_value, list):
            raw_items = skills_value
        else:
            raw_items = re.split(r'[,\n;]+', str(skills_value))

        normalized = []
        seen = set()
        for raw in raw_items:
            canonical = StudentProfile._canonicalize_skill(raw)
            if not canonical:
                continue
            key = canonical.lower()
            if key in seen:
                continue
            seen.add(key)
            normalized.append(canonical)

        return normalized
    
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
            return StudentProfile._normalize_skills_input(profile['skills'])
        return []
    
    @staticmethod
    def add_skills(user_id, new_skills):
        """Add new skills to student profile"""
        current_skills = StudentProfile.get_skills_list(user_id)
        incoming_skills = StudentProfile._normalize_skills_input(new_skills)

        seen = {s.lower() for s in current_skills}
        merged_skills = list(current_skills)
        for skill in incoming_skills:
            if skill.lower() in seen:
                continue
            merged_skills.append(skill)
            seen.add(skill.lower())

        skills_str = ', '.join(merged_skills)

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
