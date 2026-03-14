"""
Check predictions in database to debug salary issue
"""

import sqlite3

# Connect to database
conn = sqlite3.connect('placement_portal.db')
cursor = conn.cursor()

# Get all predictions
cursor.execute("""
    SELECT 
        id,
        cgpa,
        branch,
        internship_count,
        placement_probability,
        expected_salary,
        created_at
    FROM predictions
    ORDER BY id DESC
    LIMIT 15
""")

predictions = cursor.fetchall()

print("="*100)
print("Recent Salary Predictions from Database")
print("="*100)
print(f"{'ID':<5} {'CGPA':<6} {'Branch':<25} {'Internships':<12} {'Probability':<12} {'Salary':<10} {'Date':<20}")
print("-"*100)

for pred in predictions:
    print(f"{pred[0]:<5} {pred[1]:<6.2f} {pred[2]:<25} {pred[3]:<12} {pred[4]:<12.2f} {pred[5]:<10.2f} {pred[6]:<20}")

conn.close()

print("\n" + "="*100)
print("Analysis:")
print("="*100)

if predictions:
    salaries = [p[5] for p in predictions]
    unique_salaries = set(salaries)
    
    print(f"Total predictions: {len(predictions)}")
    print(f"Unique salary values: {len(unique_salaries)}")
    print(f"Salary values: {unique_salaries}")
    
    if len(unique_salaries) == 1:
        print("\n⚠ ALL PREDICTIONS HAVE THE SAME SALARY!")
        print(f"   Constant value: ₹ {salaries[0]:.2f} LPA")
        
        # Check if other values vary
        cgpas = set(p[1] for p in predictions)
        internships = set(p[3] for p in predictions)
        probabilities = set(p[4] for p in predictions)
        
        print(f"\nInput variation:")
        print(f"  Different CGPA values: {cgpas}")
        print(f"  Different internship counts: {internships}")
        print(f"  Different probabilities: {probabilities}")
