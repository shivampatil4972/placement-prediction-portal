import pytest
from resume_parser import ResumeParser

def test_extract_skills_exact_match():
    """Test standard keyword matching"""
    text = "I have 5 years of experience writing code in Python and Java. I use MySQL databases."
    skills = ResumeParser.extract_skills(text)
    
    assert "Python" in skills
    assert "Java" in skills
    assert "MySQL" in skills
    assert "C++" not in skills

def test_extract_skills_fuzzy_match():
    """Test fuzzy matching for misspelled skills"""
    # Misspelling JavaScript, Node.js and TensorFlow
    text = "Proficient in Jvascript, Node js, and TensroFlow."
    skills = ResumeParser.extract_skills(text)
    
    assert "JavaScript" in skills
    assert "Node.js" in skills
    assert "TensorFlow" in skills
    
def test_skill_categories():
    """Test that skill categorization works properly"""
    skills = ["Python", "React", "Docker", "Machine Learning"]
    categories = ResumeParser.get_skill_categories(skills)
    
    assert "Python" in categories.get("Programming Languages", [])
    assert "React" in categories.get("Web Technologies", [])
    assert "Docker" in categories.get("Cloud & DevOps", [])
    assert "Machine Learning" in categories.get("Data Science & ML", [])
