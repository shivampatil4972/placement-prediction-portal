"""
Test script to debug salary model predictions
"""

import pickle
import sys
import numpy as np

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Load the salary model
try:
    with open('salary_model.pkl', 'rb') as f:
        salary_model = pickle.load(f)
    print("\n✓ Salary model loaded successfully")
    print(f"Model type: {type(salary_model)}")
    print(f"Model class: {salary_model.__class__.__name__}")
except Exception as e:
    print(f"\n✗ Error loading salary model: {e}")
    print(f"Error type: {type(e).__name__}")
    salary_model = None
    
# Even if sklearn not available, show the model object
if salary_model:
    print("\nModel details:")
    print(f"  Has predict method: {hasattr(salary_model, 'predict')}")
    print(f"  Has fit method: {hasattr(salary_model, 'fit')}")

if salary_model:
    # Test with different inputs
    test_cases = [
        {'cgpa': 9.8, 'internships': 20, 'prob': 98.5, 'desc': 'High performer'},
        {'cgpa': 9.1, 'internships': 10, 'prob': 95.2, 'desc': 'Good performer'},
        {'cgpa': 8.5, 'internships': 5, 'prob': 85.0, 'desc': 'Average performer'},
        {'cgpa': 7.0, 'internships': 2, 'prob': 70.0, 'desc': 'Below average'},
    ]
    
    print("\n" + "="*60)
    print("Testing Salary Model Predictions")
    print("="*60)
    
    for test in test_cases:
        features = np.array([[test['cgpa'], test['internships'], test['prob']]])
        try:
            prediction = salary_model.predict(features)[0]
            print(f"\n{test['desc']}:")
            print(f"  Input: CGPA={test['cgpa']}, Internships={test['internships']}, Prob={test['prob']}%")
            print(f"  Predicted Salary: ₹ {prediction:.2f} LPA")
        except Exception as e:
            print(f"\n{test['desc']}: Error - {e}")
    
    print("\n" + "="*60)
    
    # Check if model has attributes
    print("\nModel attributes:")
    if hasattr(salary_model, '__dict__'):
        for key, value in salary_model.__dict__.items():
            print(f"  {key}: {value}")
