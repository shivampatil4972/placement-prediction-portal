"""
Machine Learning Model Training Script
Trains placement and salary prediction models with synthetic data
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
import pickle
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("PLACEMENT PORTAL - ML MODEL TRAINING")
print("="*80)

# ============================================================================
# GENERATE SYNTHETIC TRAINING DATA
# ============================================================================

print("\n[1/5] Generating synthetic training data...")

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples - large dataset for high accuracy
n_samples = 10000

# Generate features
data = []

for i in range(n_samples):
    # CGPA: 5.0 to 10.0 with normal distribution around 7.5
    cgpa = np.clip(np.random.normal(7.5, 1.2), 5.0, 10.0)
    
    # Branch (encoded)
    # 5=CS, 4=IT, 3=Electronics, 2=Electrical, 1=Mechanical, 0=Civil
    branch_code = np.random.choice([5, 4, 3, 2, 1, 0], p=[0.25, 0.20, 0.20, 0.15, 0.12, 0.08])
    
    # Higher CGPA and better branches tend to have more internships
    base_internships = int(np.random.poisson(2))
    if cgpa > 8.5:
        base_internships += np.random.randint(0, 3)
    if branch_code >= 4:
        base_internships += np.random.randint(0, 2)
    internship_count = min(base_internships, 20)
    
    # Projects - correlated with CGPA and internships
    base_projects = int(np.random.poisson(3))
    if cgpa > 8.0:
        base_projects += np.random.randint(0, 3)
    if internship_count > 3:
        base_projects += np.random.randint(0, 2)
    project_count = min(base_projects, 25)
    
    # Certifications
    base_certs = int(np.random.poisson(5))
    if cgpa > 8.5:
        base_certs += np.random.randint(0, 5)
    certification_count = min(base_certs, 30)
    
    # Skills - more for CS/IT students
    base_skills = int(np.random.poisson(5))
    if branch_code >= 4:
        base_skills += np.random.randint(0, 3)
    if cgpa > 8.0:
        base_skills += np.random.randint(0, 2)
    skill_count = min(base_skills, 15)
    
    # ========================================================================
    # PLACEMENT PROBABILITY CALCULATION (Target Variable)
    # ========================================================================
    # Rule-based with some randomness for realism
    
    placement_score = 0.0
    
    # CGPA contribution (40% weight)
    placement_score += (cgpa / 10.0) * 40
    
    # Branch contribution (15% weight)
    placement_score += (branch_code / 5.0) * 15
    
    # Internships (15% weight)
    placement_score += min(internship_count / 10.0, 1.0) * 15
    
    # Projects (10% weight)
    placement_score += min(project_count / 10.0, 1.0) * 10
    
    # Certifications (10% weight)
    placement_score += min(certification_count / 15.0, 1.0) * 10
    
    # Skills (10% weight)
    placement_score += min(skill_count / 10.0, 1.0) * 10
    
    # Add small random noise
    placement_score += np.random.uniform(-3, 3)
    
    # Convert to probability (0-100)
    placement_probability = np.clip(placement_score, 0, 100)
    
    # Binary placement outcome (placed=1, not placed=0)
    # Higher probability means more likely to be placed
    placed = 1 if placement_probability > 50 else 0
    
    # Add some uncertainty - even high scorers might not get placed (10% randomness)
    if np.random.random() < 0.1:
        placed = 1 - placed
    
    # ========================================================================
    # SALARY CALCULATION (Target Variable for Regression)
    # ========================================================================
    
    # Branch salary multipliers
    branch_multipliers = {0: 0.7, 1: 0.8, 2: 0.9, 3: 1.0, 4: 1.2, 5: 1.3}
    multiplier = branch_multipliers[branch_code]
    
    # Base calculation
    base_salary = 3.5
    cgpa_boost = (cgpa - 6) * 0.6
    internship_boost = min(internship_count * 0.4, 2.0)
    prob_boost = (placement_probability / 100) * 1.5
    
    salary = (base_salary + cgpa_boost + internship_boost + prob_boost) * multiplier
    
    # Add small random variation (±5%)
    salary = salary * np.random.uniform(0.95, 1.05)
    
    # Clip to reasonable range
    salary = np.clip(salary, 2.5, 25.0)
    
    # Round to 2 decimals
    salary = round(salary, 2)
    
    # Store data
    data.append([
        cgpa, branch_code, internship_count, project_count,
        certification_count, skill_count, placement_probability, 
        placed, salary
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    'cgpa', 'branch_code', 'internship_count', 'project_count',
    'certification_count', 'skill_count', 'placement_probability',
    'placed', 'salary'
])

print(f"✓ Generated {len(df)} training samples")
print(f"\nDataset Statistics:")
print(f"  CGPA range: {df['cgpa'].min():.2f} - {df['cgpa'].max():.2f}")
print(f"  Placement rate: {df['placed'].mean()*100:.1f}%")
print(f"  Avg salary: ₹ {df['salary'].mean():.2f} LPA")
print(f"  Salary range: ₹ {df['salary'].min():.2f} - ₹ {df['salary'].max():.2f} LPA")

# ============================================================================
# TRAIN PLACEMENT PREDICTION MODEL (Classification)
# ============================================================================

print("\n[2/5] Training Placement Prediction Model...")

# Features for placement
X_placement = df[['cgpa', 'branch_code', 'internship_count', 'project_count', 
                   'certification_count', 'skill_count']]
y_placement = df['placed']

# Split data
X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X_placement, y_placement, test_size=0.2, random_state=42, stratify=y_placement
)

# Train Random Forest Classifier (best for this type of data)
placement_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

placement_model.fit(X_train_p, y_train_p)

# Evaluate
y_pred_p = placement_model.predict(X_test_p)
accuracy = accuracy_score(y_test_p, y_pred_p)

print(f"✓ Placement Model Trained")
print(f"  Algorithm: Random Forest Classifier")
print(f"  Training samples: {len(X_train_p)}")
print(f"  Testing samples: {len(X_test_p)}")
print(f"  Accuracy: {accuracy*100:.2f}%")

# Detailed metrics
print("\nClassification Report:")
print(classification_report(y_test_p, y_pred_p, target_names=['Not Placed', 'Placed']))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X_placement.columns,
    'importance': placement_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
for idx, row in feature_importance.iterrows():
    print(f"  {row['feature']:<20}: {row['importance']*100:.1f}%")

# Save model
with open('placement_model.pkl', 'wb') as f:
    pickle.dump(placement_model, f)
print("\n✓ Placement model saved as 'placement_model.pkl'")

# ============================================================================
# TRAIN SALARY PREDICTION MODEL (Regression)
# ============================================================================

print("\n[3/5] Training Salary Prediction Model...")

# Features for salary (use placement probability as feature)
X_salary = df[['cgpa', 'internship_count', 'placement_probability']]
y_salary = df['salary']

# Split data
X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(
    X_salary, y_salary, test_size=0.2, random_state=42
)

# Train Gradient Boosting Regressor
salary_model = GradientBoostingRegressor(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42
)

salary_model.fit(X_train_s, y_train_s)

# Evaluate
y_pred_s = salary_model.predict(X_test_s)
mse = mean_squared_error(y_test_s, y_pred_s)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_s, y_pred_s)

print(f"✓ Salary Model Trained")
print(f"  Algorithm: Gradient Boosting Regressor")
print(f"  Training samples: {len(X_train_s)}")
print(f"  Testing samples: {len(X_test_s)}")
print(f"  R² Score: {r2*100:.2f}%")
print(f"  RMSE: ₹ {rmse:.2f} LPA")
print(f"  Mean Absolute Error: ₹ {np.mean(np.abs(y_test_s - y_pred_s)):.2f} LPA")

# Feature importance
feature_importance_salary = pd.DataFrame({
    'feature': X_salary.columns,
    'importance': salary_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
for idx, row in feature_importance_salary.iterrows():
    print(f"  {row['feature']:<25}: {row['importance']*100:.1f}%")

# Save model
with open('salary_model.pkl', 'wb') as f:
    pickle.dump(salary_model, f)
print("\n✓ Salary model saved as 'salary_model.pkl'")

# ============================================================================
# TEST MODELS WITH SAMPLE PREDICTIONS
# ============================================================================

print("\n[4/5] Testing Models with Sample Data...")

test_samples = [
    {'cgpa': 9.8, 'branch': 'CS', 'branch_code': 5, 'internships': 20, 'projects': 22, 'certs': 15, 'skills': 10, 'desc': 'Excellent Student'},
    {'cgpa': 9.1, 'branch': 'CS', 'branch_code': 5, 'internships': 5, 'projects': 10, 'certs': 10, 'skills': 8, 'desc': 'Very Good Student'},
    {'cgpa': 8.5, 'branch': 'IT', 'branch_code': 4, 'internships': 10, 'projects': 15, 'certs': 12, 'skills': 9, 'desc': 'Good IT Student'},
    {'cgpa': 7.5, 'branch': 'Electronics', 'branch_code': 3, 'internships': 3, 'projects': 5, 'certs': 8, 'skills': 6, 'desc': 'Average Student'},
    {'cgpa': 6.5, 'branch': 'Mechanical', 'branch_code': 1, 'internships': 1, 'projects': 2, 'certs': 5, 'skills': 4, 'desc': 'Below Average Student'},
]

print("\n" + "="*80)
for sample in test_samples:
    # Placement prediction
    X_p = np.array([[sample['cgpa'], sample['branch_code'], sample['internships'], 
                     sample['projects'], sample['certs'], sample['skills']]])
    placement_prob = placement_model.predict_proba(X_p)[0][1] * 100
    
    # Salary prediction
    X_s = np.array([[sample['cgpa'], sample['internships'], placement_prob]])
    predicted_salary = salary_model.predict(X_s)[0]
    
    print(f"\n{sample['desc']} ({sample['branch']}):")
    print(f"  CGPA: {sample['cgpa']}, Internships: {sample['internships']}, Projects: {sample['projects']}")
    print(f"  Placement Probability: {placement_prob:.2f}%")
    print(f"  Expected Salary: ₹ {predicted_salary:.2f} LPA")

# ============================================================================
# SAVE TRAINING DATA FOR REFERENCE
# ============================================================================

print("\n\n[5/5] Saving training data...")
df.to_csv('training_data.csv', index=False)
print(f"✓ Training data saved as 'training_data.csv' ({len(df)} samples)")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*80)
print("TRAINING COMPLETE!")
print("="*80)
print(f"\n✓ Placement Model: {accuracy*100:.2f}% accuracy")
print(f"✓ Salary Model: {r2*100:.2f}% R² score (variance explained)")
print(f"\nFiles created:")
print(f"  • placement_model.pkl - Placement prediction model")
print(f"  • salary_model.pkl - Salary prediction model")
print(f"  • training_data.csv - Training dataset ({len(df)} samples)")
print(f"\nNext steps:")
print(f"  1. Restart your Flask application: python app.py")
print(f"  2. Test predictions with different student profiles")
print(f"  3. Models will now provide accurate, varying predictions!")
print("\n" + "="*80)
