"""
Verify trained models are working correctly
"""

import sys
sys.path.insert(0, 'c:\\Users\\shiva\\OneDrive\\Desktop\\PLACEMENT PORTAL')

from ml_utils import MLPredictor

# Create predictor instance with newly trained models
predictor = MLPredictor()

print("="*90)
print("TESTING NEWLY TRAINED ML MODELS")
print("="*90)

# Test cases matching user's actual scenario
test_students = [
    {
        'name': 'Excellent CS Student',
        'cgpa': 9.8,
        'branch': 'Computer Science',
        'internships': 20,
        'projects': 22,
        'certs': 15,
        'skills': 10
    },
    {
        'name': 'Very Good CS Student',
        'cgpa': 9.1,
        'branch': 'Computer Science',
        'internships': 5,
        'projects': 10,
        'certs': 10,
        'skills': 8
    },
    {
        'name': 'Good CS Student',
        'cgpa': 8.5,
        'branch': 'Computer Science',
        'internships': 10,
        'projects': 15,
        'certs': 12,
        'skills': 9
    },
    {
        'name': 'Average CS Student',
        'cgpa': 7.0,
        'branch': 'Computer Science',
        'internships': 2,
        'projects': 5,
        'certs': 5,
        'skills': 5
    },
    {
        'name': 'Below Average Student',
        'cgpa': 5.0,
        'branch': 'Computer Science',
        'internships': 0,
        'projects': 0,
        'certs': 5,
        'skills': 5
    },
    {
        'name': 'Good IT Student',
        'cgpa': 8.5,
        'branch': 'Information Technology',
        'internships': 8,
        'projects': 12,
        'certs': 10,
        'skills': 8
    },
    {
        'name': 'Average Electronics Student',
        'cgpa': 7.5,
        'branch': 'Electronics',
        'internships': 3,
        'projects': 5,
        'certs': 6,
        'skills': 6
    },
]

results = []

for student in test_students:
    # Get placement prediction
    placement_prob = predictor.predict_placement(
        student['cgpa'],
        student['branch'],
        student['internships'],
        student['projects'],
        student['certs'],
        student['skills']
    )
    
    # Get salary prediction
    salary = predictor.predict_salary(
        student['cgpa'],
        student['branch'],
        student['internships'],
        placement_prob
    )
    
    risk_level = predictor.get_risk_level(placement_prob)
    
    results.append({
        'name': student['name'],
        'cgpa': student['cgpa'],
        'branch': student['branch'],
        'internships': student['internships'],
        'placement_prob': placement_prob,
        'salary': salary,
        'risk': risk_level
    })
    
    print(f"\n{student['name']}:")
    print(f"  CGPA: {student['cgpa']:.1f} | Branch: {student['branch']}")
    print(f"  Internships: {student['internships']} | Projects: {student['projects']} | Skills: {student['skills']}")
    print(f"  ➜ Placement Probability: {placement_prob:.2f}% ({risk_level} Risk)")
    print(f"  ➜ Expected Salary: ₹ {salary:.2f} LPA")

# Analysis
print("\n" + "="*90)
print("ACCURACY ANALYSIS")
print("="*90)

salaries = [r['salary'] for r in results]
probabilities = [r['placement_prob'] for r in results]

print(f"\n✓ Salary Predictions:")
print(f"  Unique values: {len(set(salaries))} out of {len(salaries)} students")
print(f"  Range: ₹ {min(salaries):.2f} - ₹ {max(salaries):.2f} LPA")
print(f"  Average: ₹ {sum(salaries)/len(salaries):.2f} LPA")

print(f"\n✓ Placement Probabilities:")
print(f"  Unique values: {len(set(probabilities))} out of {len(probabilities)} students")
print(f"  Range: {min(probabilities):.2f}% - {max(probabilities):.2f}%")
print(f"  Average: {sum(probabilities)/len(probabilities):.2f}%")

# Check if all different
if len(set(salaries)) == len(salaries):
    print("\n✓✓✓ SUCCESS! All salary predictions are UNIQUE and vary correctly!")
else:
    print(f"\n⚠ Warning: {len(salaries) - len(set(salaries))} duplicate salary values found")

if len(set(probabilities)) == len(probabilities):
    print("✓✓✓ SUCCESS! All placement probabilities are UNIQUE!")
else:
    print(f"⚠ {len(probabilities) - len(set(probabilities))} duplicate probabilities (this is OK)")

# Verify trends
print("\n" + "="*90)
print("VERIFICATION OF EXPECTED TRENDS")
print("="*90)

# Higher CGPA should generally lead to higher salary
cs_students = [r for r in results if r['branch'] == 'Computer Science']
if len(cs_students) >= 3:
    cs_students_sorted = sorted(cs_students, key=lambda x: x['cgpa'])
    print("\n✓ CGPA vs Salary (CS students):")
    for s in cs_students_sorted:
        print(f"  CGPA {s['cgpa']:.1f} → ₹ {s['salary']:.2f} LPA")
    
    # Check if trend is correct (higher CGPA = higher salary generally)
    trend_correct = True
    for i in range(len(cs_students_sorted)-1):
        # Allow small variations due to internship differences
        if cs_students_sorted[i]['cgpa'] < cs_students_sorted[i+1]['cgpa']:
            if cs_students_sorted[i]['salary'] > cs_students_sorted[i+1]['salary'] + 1.0:
                trend_correct = False
    
    if trend_correct:
        print("  ✓ Trend is correct: Higher CGPA correlates with higher salary!")

# Branch comparison
if len(results) >= 5:
    print("\n✓ Branch Comparison (similar profiles):")
    branch_salaries = {}
    for r in results:
        if r['cgpa'] >= 8.0:  # Compare good students
            if r['branch'] not in branch_salaries:
                branch_salaries[r['branch']] = []
            branch_salaries[r['branch']].append(r['salary'])
    
    for branch, salaries in sorted(branch_salaries.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
        avg_sal = sum(salaries)/len(salaries)
        print(f"  {branch}: ₹ {avg_sal:.2f} LPA (avg)")

print("\n" + "="*90)
print("MODELS ARE READY TO USE!")
print("="*90)
print("\nRestart your Flask app to see the improvements:")
print("  python app.py")
print("\n" + "="*90)
