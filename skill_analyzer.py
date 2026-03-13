"""
Skill Gap Analysis Utility
Analyzes student skills and provides recommendations
"""

from config import Config

class SkillGapAnalyzer:
    """Analyze skill gaps and provide recommendations"""
    
    @staticmethod
    def analyze(profile_data, placement_probability):
        """
        Perform comprehensive skill gap analysis
        
        Args:
            profile_data: Student profile dictionary
            placement_probability: Current placement probability
        
        Returns:
            Dictionary with analysis results
        """
        
        branch = profile_data.get('branch', '')
        current_skills = profile_data.get('skills', '')
        cgpa = profile_data.get('cgpa', 0)
        internship_count = profile_data.get('internship_count', 0)
        project_count = profile_data.get('project_count', 0)
        certification_count = profile_data.get('certification_count', 0)
        
        # Parse current skills
        if current_skills:
            current_skills_list = [s.strip() for s in current_skills.split(',')]
        else:
            current_skills_list = []
        
        # Get important skills for branch
        important_skills = Config.BRANCH_IMPORTANT_SKILLS.get(branch, 
                                                               Config.BRANCH_IMPORTANT_SKILLS['Computer Science'])
        
        # Find missing skills
        missing_skills = [skill for skill in important_skills if skill not in current_skills_list]
        
        # Generate recommendations
        recommendations = []
        priority = 'Medium'
        
        # CGPA-based recommendations
        if cgpa < 7.0:
            recommendations.append("Focus on improving CGPA to at least 7.0 for better placement opportunities.")
            priority = 'High'
        elif cgpa < 8.0:
            recommendations.append("Good CGPA! Aim for 8.0+ to access top-tier companies.")
        
        # Internship recommendations
        if internship_count == 0:
            recommendations.append("URGENT: Complete at least 1-2 internships before placements. This significantly improves placement chances.")
            priority = 'High'
        elif internship_count == 1:
            recommendations.append("Consider doing one more internship to strengthen your profile.")
        else:
            recommendations.append("Excellent internship experience! Highlight your learnings in interviews.")
        
        # Project recommendations
        if project_count < 2:
            recommendations.append("Build 2-3 strong projects showcasing your technical skills. Quality matters more than quantity.")
            if priority != 'High':
                priority = 'Medium'
        elif project_count >= 3:
            recommendations.append("Great project portfolio! Make sure they are well-documented on GitHub.")
        
        # Certification recommendations
        if certification_count == 0:
            recommendations.append("Consider getting 1-2 relevant certifications (e.g., AWS, Google Cloud, Coursera courses).")
        
        # Skill-based recommendations
        if missing_skills:
            skill_recommendation = f"Learn these important skills for {branch}: {', '.join(missing_skills[:3])}"
            recommendations.append(skill_recommendation)
            
            if len(missing_skills) > 3:
                priority = 'High'
        
        if len(current_skills_list) < 5:
            recommendations.append("Expand your skill set. Aim for at least 6-8 relevant technical skills.")
            if priority != 'High':
                priority = 'Medium'
        
        # Data Structures & Algorithms
        if 'DSA' not in current_skills_list and 'Data Structures' not in current_skills_list and 'Algorithms' not in current_skills_list:
            recommendations.append("Master Data Structures and Algorithms - crucial for technical interviews.")
            priority = 'High'
        
        # Git/GitHub
        if 'Git' not in current_skills_list and 'GitHub' not in current_skills_list:
            recommendations.append("Learn Git and create a GitHub profile to showcase your projects.")
        
        # Communication skills
        recommendations.append("Practice communication skills, aptitude, and mock interviews regularly.")
        
        # Probability-based recommendations
        if placement_probability < 40:
            recommendations.insert(0, "⚠️ URGENT: Your placement probability is low. Focus on immediate improvements in internships, projects, and skill development.")
            priority = 'High'
        elif placement_probability < 70:
            recommendations.insert(0, "Your placement chances are moderate. Follow the recommendations below to improve your profile.")
        else:
            recommendations.insert(0, "✅ Great profile! Maintain your momentum and prepare well for interviews.")
            if priority == 'Medium':
                priority = 'Low'
        
        # Company-specific recommendations
        if placement_probability >= 70 and cgpa >= 8.0:
            recommendations.append("You're eligible for top-tier companies. Prepare for advanced problem-solving and system design.")
        
        return {
            'missing_skills': missing_skills,
            'missing_skills_str': ', '.join(missing_skills) if missing_skills else 'None',
            'recommendations': recommendations,
            'priority': priority,
            'skill_coverage': round((len(current_skills_list) / len(important_skills)) * 100, 1) if important_skills else 100
        }
    
    @staticmethod
    def get_improvement_areas(profile_data):
        """Get quick list of improvement areas"""
        areas = []
        
        if profile_data.get('cgpa', 0) < 7.0:
            areas.append('CGPA')
        
        if profile_data.get('internship_count', 0) < 2:
            areas.append('Internships')
        
        if profile_data.get('project_count', 0) < 2:
            areas.append('Projects')
        
        skills = profile_data.get('skills', '')
        skill_count = len(skills.split(',')) if skills else 0
        
        if skill_count < 5:
            areas.append('Technical Skills')
        
        if profile_data.get('certification_count', 0) == 0:
            areas.append('Certifications')
        
        return areas
    
    @staticmethod
    def suggest_skills_to_learn(branch, current_skills_list):
        """Suggest top 3 skills to learn based on branch"""
        important_skills = Config.BRANCH_IMPORTANT_SKILLS.get(branch, 
                                                               Config.BRANCH_IMPORTANT_SKILLS['Computer Science'])
        
        missing = [skill for skill in important_skills if skill not in current_skills_list]
        
        return missing[:3] if missing else []


# Convenience instance
skill_analyzer = SkillGapAnalyzer()
