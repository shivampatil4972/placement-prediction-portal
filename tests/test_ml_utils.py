import pytest
from ml_utils import MLPredictor

@pytest.fixture
def predictor():
    """Provide a fresh MLPredictor instance for each test"""
    return MLPredictor()

def test_fallback_placement_prediction(predictor):
    """Test that the rule-based fallback logic returns a valid probability between 0 and 100"""
    prob = predictor._fallback_placement_prediction(
        cgpa=8.5, 
        internship_count=2, 
        project_count=3, 
        certification_count=1, 
        skill_count=5
    )
    assert 0 <= prob <= 100
    assert prob > 50  # A strong profile should have > 50% chance

def test_fallback_salary_prediction(predictor):
    """Test that the fallback salary logic respects bounds (2.5 - 25 LPA)"""
    # Test a strong profile
    salary_high = predictor.predict_salary(
        cgpa=9.5, 
        branch='Computer Science', 
        internship_count=5, 
        placement_probability=95.0
    )
    assert 2.5 <= salary_high <= 25.0
    
    # Test a weak profile
    salary_low = predictor.predict_salary(
        cgpa=4.0, 
        branch='Mechanical', 
        internship_count=0, 
        placement_probability=20.0
    )
    assert 2.5 <= salary_low <= 25.0
    assert salary_high > salary_low  # Better profile should get better salary

def test_calibrate_probability(predictor):
    """Test that guardrails prevent unrealistic probabilities"""
    # Very weak profile shouldn't get 90% even if model is acting weird
    calibrated_prob = predictor._calibrate_probability(
        model_probability=0.99,  # Assume model went crazy and predicts 99%
        cgpa=4.5, 
        branch_code=1, 
        internship_count=0, 
        project_count=0, 
        certification_count=0, 
        skill_count=1
    )
    # The guardrail in _calibrate_probability limits weak profiles
    assert calibrated_prob <= 45.0
