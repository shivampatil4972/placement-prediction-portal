"""
ML Model Generator
Creates sample placement and salary prediction models
Run this script once to generate the .pkl model files
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

print("=" * 60)
print("PLACEMENT PORTAL - ML MODEL GENERATOR")
print("=" * 60)
print("\nGenerating synthetic training data...")

# Generate synthetic training data
np.random.seed(42)
n_samples = 1000

# Generate features
data = {
    'cgpa': np.random.uniform(5.0, 10.0, n_samples),
    'branch': np.random.choice([0, 1, 2, 3, 4, 5], n_samples),  # Already encoded
    'internship_count': np.random.randint(0, 5, n_samples),
    'project_count': np.random.randint(0, 8, n_samples),
    'certification_count': np.random.randint(0, 6, n_samples),
    'skill_count': np.random.randint(2, 15, n_samples)
}

df = pd.DataFrame(data)

# Generate target variable (placement) based on features with some logic
placement_probability = (
    (df['cgpa'] - 5) / 5 * 30 +  # CGPA contributes up to 30%
    df['internship_count'] * 10 +  # Each internship adds 10%
    df['project_count'] * 5 +  # Each project adds 5%
    df['certification_count'] * 3 +  # Each cert adds 3%
    df['skill_count'] * 2 +  # Skills add up to 20%
    df['branch'] * 3 +  # Branch factor
    np.random.normal(0, 10, n_samples)  # Random noise
)

# Normalize to 0-100 and clip
placement_probability = np.clip(placement_probability, 0, 100)

# Create binary placement target (1 if probability > 50, else 0)
df['placed'] = (placement_probability > 50).astype(int)

# Create salary target (in LPA)
df['salary'] = (
    2.5 +  # Base salary
    (df['cgpa'] - 6) * 0.5 +  # CGPA boost
    df['internship_count'] * 0.8 +  # Internship boost
    df['branch'] * 0.3 +  # Branch boost
    (placement_probability / 100) * 2 +  # Probability boost
    np.random.normal(0, 1, n_samples)  # Noise
)

# Clip salary between 2.5 and 25 LPA
df['salary'] = np.clip(df['salary'], 2.5, 25)

print(f"✓ Generated {n_samples} training samples")
print(f"✓ Placement distribution: {df['placed'].value_counts().to_dict()}")
print(f"✓ Salary range: {df['salary'].min():.2f} - {df['salary'].max():.2f} LPA")

# Prepare features and targets
X = df[['cgpa', 'branch', 'internship_count', 'project_count', 
        'certification_count', 'skill_count']]

y_placement = df['placed']
y_salary = df['salary']

# Split data
X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X, y_placement, test_size=0.2, random_state=42
)

X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(
    X, y_salary, test_size=0.2, random_state=42
)

print("\n" + "=" * 60)
print("Training Placement Prediction Model...")
print("=" * 60)

# Train placement model (Classification)
placement_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    min_samples_split=5
)

placement_model.fit(X_train_p, y_train_p)

# Evaluate
train_score_p = placement_model.score(X_train_p, y_train_p)
test_score_p = placement_model.score(X_test_p, y_test_p)

print(f"✓ Training Accuracy: {train_score_p*100:.2f}%")
print(f"✓ Testing Accuracy: {test_score_p*100:.2f}%")

# Save placement model
with open('placement_model.pkl', 'wb') as f:
    pickle.dump(placement_model, f)

print("✓ Placement model saved as 'placement_model.pkl'")

print("\n" + "=" * 60)
print("Training Salary Prediction Model...")
print("=" * 60)

# Train salary model (Regression)
salary_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    min_samples_split=5
)

salary_model.fit(X_train_s, y_train_s)

# Evaluate
train_score_s = salary_model.score(X_train_s, y_train_s)
test_score_s = salary_model.score(X_test_s, y_test_s)

print(f"✓ Training R² Score: {train_score_s:.4f}")
print(f"✓ Testing R² Score: {test_score_s:.4f}")

# Save salary model
with open('salary_model.pkl', 'wb') as f:
    pickle.dump(salary_model, f)

print("✓ Salary model saved as 'salary_model.pkl'")

print("\n" + "=" * 60)
print("Testing Models with Sample Predictions...")
print("=" * 60)

# Test predictions
test_cases = [
    {
        'name': 'High Performer',
        'data': np.array([[9.0, 5, 3, 5, 3, 12]])
    },
    {
        'name': 'Average Student',
        'data': np.array([[7.5, 3, 1, 2, 1, 6]])
    },
    {
        'name': 'Needs Improvement',
        'data': np.array([[6.0, 2, 0, 1, 0, 3]])
    }
]

for case in test_cases:
    prob = placement_model.predict_proba(case['data'])[0][1] * 100
    salary = salary_model.predict(case['data'])[0]
    
    print(f"\n{case['name']}:")
    print(f"  Placement Probability: {prob:.2f}%")
    print(f"  Expected Salary: ₹ {salary:.2f} LPA")

print("\n" + "=" * 60)
print("✓ MODEL GENERATION COMPLETE!")
print("=" * 60)
print("\nFiles created:")
print("  1. placement_model.pkl - Classification model for placement prediction")
print("  2. salary_model.pkl - Regression model for salary prediction")
print("\nYou can now run the Flask application!")
print("=" * 60)
