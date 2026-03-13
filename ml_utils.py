"""
Machine Learning Utility
Handles model loading and predictions
"""

import pickle
import numpy as np
from config import Config

class MLPredictor:
    """ML model handler for placement and salary prediction"""
    
    def __init__(self):
        self.placement_model = None
        self.salary_model = None
        self.load_models()
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            with open(Config.PLACEMENT_MODEL_PATH, 'rb') as f:
                self.placement_model = pickle.load(f)
            print("Placement model loaded successfully")
        except Exception as e:
            print(f"Error loading placement model: {str(e)}")
            print("Using fallback prediction method")
        
        try:
            with open(Config.SALARY_MODEL_PATH, 'rb') as f:
                self.salary_model = pickle.load(f)
            print("Salary model loaded successfully")
        except Exception as e:
            print(f"Error loading salary model: {str(e)}")
            print("Using fallback salary estimation")
    
    def predict_placement(self, cgpa, branch, internship_count, project_count, 
                         certification_count, skill_count):
        """
        Predict placement probability
        
        Args:
            cgpa: Student CGPA (0-10)
            branch: Engineering branch
            internship_count: Number of internships
            project_count: Number of projects
            certification_count: Number of certifications
            skill_count: Number of skills
        
        Returns:
            Placement probability (0-100)
        """
        
        # Branch encoding (simple ordinal encoding)
        branch_encoding = {
            'Computer Science': 5,
            'Information Technology': 4,
            'Electronics': 3,
            'Electrical': 2,
            'Mechanical': 1,
            'Civil': 0
        }
        branch_code = branch_encoding.get(branch, 2)
        
        # Prepare features
        features = np.array([[
            cgpa,
            branch_code,
            internship_count,
            project_count,
            certification_count,
            skill_count
        ]])
        
        try:
            if self.placement_model:
                # Use actual model
                probability = self.placement_model.predict_proba(features)[0][1] * 100
            else:
                # Fallback: rule-based prediction
                probability = self._fallback_placement_prediction(
                    cgpa, internship_count, project_count, 
                    certification_count, skill_count
                )
            
            return round(min(100, max(0, probability)), 2)
            
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return self._fallback_placement_prediction(
                cgpa, internship_count, project_count, 
                certification_count, skill_count
            )
    
    def predict_salary(self, cgpa, branch, internship_count, placement_probability):
        """
        Predict expected salary using trained ML model
        
        Returns:
            Predicted salary in lakhs per annum
        """
        
        # Branch salary multiplier (only used for fallback)
        branch_multiplier = {
            'Computer Science': 1.3,
            'Information Technology': 1.2,
            'Electronics': 1.0,
            'Electrical': 0.9,
            'Mechanical': 0.8,
            'Civil': 0.7
        }
        multiplier = branch_multiplier.get(branch, 1.0)
        
        try:
            if self.salary_model:
                # Use trained ML model (preferred method)
                features = np.array([[cgpa, internship_count, placement_probability]])
                salary = self.salary_model.predict(features)[0]
                
                # Apply branch multiplier to model prediction
                salary = salary * multiplier
            else:
                # Fallback: rule-based calculation
                base_salary = 3.5
                cgpa_boost = max(0, (cgpa - 6) * 0.6)
                internship_boost = min(internship_count * 0.4, 2.0)
                prob_boost = (placement_probability / 100) * 1.5
                salary = (base_salary + cgpa_boost + internship_boost + prob_boost) * multiplier
            
            # Ensure salary is within reasonable bounds (2.5 - 25 LPA)
            return round(max(2.5, min(25, salary)), 2)
            
        except Exception as e:
            print(f"Salary prediction error: {str(e)}")
            # Fallback calculation
            base_salary = 3.5
            cgpa_boost = max(0, (cgpa - 6) * 0.6)
            internship_boost = min(internship_count * 0.4, 2.0)
            prob_boost = (placement_probability / 100) * 1.5
            return round(max(2.5, min(25, (base_salary + cgpa_boost + internship_boost + prob_boost) * multiplier)), 2)
    
    def _fallback_placement_prediction(self, cgpa, internship_count, project_count, 
                                       certification_count, skill_count):
        """Fallback rule-based prediction when model is not available"""
        
        # Base score from CGPA (max 40 points)
        cgpa_score = (cgpa / 10) * 40
        
        # Internship score (max 25 points)
        internship_score = min(internship_count * 8, 25)
        
        # Project score (max 15 points)
        project_score = min(project_count * 5, 15)
        
        # Certification score (max 10 points)
        cert_score = min(certification_count * 3, 10)
        
        # Skills score (max 10 points)
        skill_score = min(skill_count * 1, 10)
        
        total_score = cgpa_score + internship_score + project_score + cert_score + skill_score
        
        return round(total_score, 2)
    
    def get_risk_level(self, probability):
        """Calculate risk level based on probability"""
        if probability >= Config.RISK_THRESHOLDS['Low']:
            return 'Low'
        elif probability >= Config.RISK_THRESHOLDS['Medium']:
            return 'Medium'
        else:
            return 'High'


# Global predictor instance
ml_predictor = MLPredictor()
