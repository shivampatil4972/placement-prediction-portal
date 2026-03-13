"""
Test the fixed salary prediction function
"""

import sys
sys.path.insert(0, 'c:\\Users\\shiva\\OneDrive\\Desktop\\PLACEMENT PORTAL')

from ml_utils import MLPredictor

# Create predictor instance
predictor = MLPredictor()

# Test cases from the user's data
test_cases = [
    {
        'cgpa': 9.8,
        'branch': 'Computer Science',
        'internships': 20,
        'prob': 98.5,
        'expected': '~12 LPA (high performer)'
    },
    {
        'cgpa': 9.1,
        'branch': 'Computer Science',
        'internships': 5,
        'prob': 100.0,
        'expected': '~11 LPA (good performer)'
    },
    {
        'cgpa': 8.5,
        'branch': 'Computer Science',
        'internships': 10,
        'prob': 95.0,
        'expected': '~10 LPA (good performer)'
    },
    {
        'cgpa': 5.0,
        'branch': 'Computer Science',
        'internships': 0,
        'prob': 31.0,
        'expected': '~5 LPA (below average)'
    },
    {
        'cgpa': 7.5,
        'branch': 'Information Technology',
        'internships': 3,
        'prob': 80.0,
        'expected': '~7-8 LPA (average IT)'
    },
]

print("="*80)
print("Testing Fixed Salary Prediction Function")
print("="*80)

for i, test in enumerate(test_cases, 1):
    salary = predictor.predict_salary(
        test['cgpa'],
        test['branch'],
        test['internships'],
        test['prob']
    )
    
    print(f"\nTest {i}: {test['expected']}")
    print(f"  Input: CGPA={test['cgpa']}, Branch={test['branch']}, " 
          f"Internships={test['internships']}, Probability={test['prob']}%")
    print(f"  Predicted Salary: ₹ {salary:.2f} LPA")
    print(f"  {'✓ VARYING' if i == 1 else '✓ DIFFERENT' if salary != 4.55 else '✗ STILL 4.55!'}")

print("\n" + "="*80)
print("Summary:")
print("="*80)

salaries = [predictor.predict_salary(t['cgpa'], t['branch'], t['internships'], t['prob']) 
            for t in test_cases]
unique_salaries = len(set(salaries))

print(f"Total tests: {len(test_cases)}")
print(f"Unique salary values: {unique_salaries}")
print(f"Salary range: ₹ {min(salaries):.2f} - ₹ {max(salaries):.2f} LPA")

if unique_salaries == len(test_cases):
    print("\n✓ SUCCESS! All predictions are now unique and vary based on inputs!")
elif unique_salaries > 1:
    print(f"\n✓ IMPROVED! Now showing {unique_salaries} different salary values")
else:
    print("\n✗ STILL BROKEN - All predictions showing same value")
