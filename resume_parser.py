"""
Resume Parsing Utility
Extracts text and skills from PDF resumes
"""

import PyPDF2
import re
from config import Config

class ResumeParser:
    """Parse PDF resumes and extract skills"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """
        Extract text content from PDF file
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Extracted text as string
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + '\n'
                
                return text.strip()
                
        except Exception as e:
            print(f"Error extracting PDF text: {str(e)}")
            return None
    
    @staticmethod
    def extract_skills(text):
        """
        Extract skills from text using keyword matching
        
        Args:
            text: Resume text content
        
        Returns:
            List of found skills
        """
        if not text:
            return []
        
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        found_skills = []
        
        # Search for each skill keyword
        for skill in Config.SKILL_KEYWORDS:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return found_skills
    
    @staticmethod
    def extract_email(text):
        """Extract email addresses from text"""
        if not text:
            return []
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        return emails
    
    @staticmethod
    def extract_phone(text):
        """Extract phone numbers from text"""
        if not text:
            return []
        
        # Pattern for Indian phone numbers
        phone_pattern = r'\b(?:\+91[-\s]?)?[6-9]\d{9}\b'
        phones = re.findall(phone_pattern, text)
        
        return phones
    
    @staticmethod
    def extract_urls(text):
        """Extract URLs from text"""
        if not text:
            return []
        
        # Pattern for GitHub and LinkedIn URLs
        url_pattern = r'https?://(?:www\.)?(?:github\.com|linkedin\.com)/[\w\-/]+'
        urls = re.findall(url_pattern, text)
        
        return urls
    
    @staticmethod
    def get_skill_categories(skills):
        """Categorize skills into groups"""
        categories = {
            'Programming Languages': [],
            'Web Technologies': [],
            'Databases': [],
            'Data Science & ML': [],
            'Cloud & DevOps': [],
            'Other': []
        }
        
        programming = ['Python', 'Java', 'JavaScript', 'C++', 'C', 'C#', 'Ruby', 'Go', 'Rust', 'PHP', 'Swift', 'Kotlin', 'TypeScript', 'Scala', 'R', 'MATLAB']
        web = ['HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js', 'Django', 'Flask', 'Spring Boot', 'ASP.NET', 'Bootstrap', 'jQuery', 'REST API', 'GraphQL', 'AJAX']
        databases = ['MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle', 'SQL Server', 'Redis', 'Cassandra', 'DynamoDB', 'Firebase']
        datascience = ['Machine Learning', 'Deep Learning', 'Neural Networks', 'TensorFlow', 'PyTorch', 'Keras', 'scikit-learn', 'Pandas', 'NumPy', 'Data Analysis', 'Data Science', 'NLP', 'Computer Vision', 'AI']
        cloud = ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'CI/CD', 'Jenkins', 'Git', 'GitHub', 'GitLab', 'Linux', 'Shell Scripting']
        
        for skill in skills:
            if skill in programming:
                categories['Programming Languages'].append(skill)
            elif skill in web:
                categories['Web Technologies'].append(skill)
            elif skill in databases:
                categories['Databases'].append(skill)
            elif skill in datascience:
                categories['Data Science & ML'].append(skill)
            elif skill in cloud:
                categories['Cloud & DevOps'].append(skill)
            else:
                categories['Other'].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    @staticmethod
    def analyze_resume(pdf_path):
        """
        Complete resume analysis
        
        Returns:
            Dictionary with extracted information
        """
        text = ResumeParser.extract_text_from_pdf(pdf_path)
        
        if not text:
            return None
        
        skills = ResumeParser.extract_skills(text)
        emails = ResumeParser.extract_email(text)
        phones = ResumeParser.extract_phone(text)
        urls = ResumeParser.extract_urls(text)
        skill_categories = ResumeParser.get_skill_categories(skills)
        
        return {
            'text': text,
            'skills': skills,
            'skill_count': len(skills),
            'skill_categories': skill_categories,
            'emails': emails,
            'phones': phones,
            'urls': urls
        }


# Convenience instance
resume_parser = ResumeParser()
