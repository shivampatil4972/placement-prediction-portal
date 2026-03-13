"""
Database Verification Script
Checks if all tables and columns exist
"""
import sqlite3

DB_FILE = 'placement_portal.db'

def verify_database():
    """Verify database schema"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        print("=== DATABASE SCHEMA VERIFICATION ===\n")
        
        # Expected schema
        expected_tables = {
            'users': ['id', 'email', 'password_hash', 'full_name', 'user_type', 'created_at', 'last_login'],
            'student_profiles': ['id', 'user_id', 'cgpa', 'branch', 'internship_count', 'project_count', 
                                'certification_count', 'skills', 'placement_target', 'created_at', 'updated_at'],
            'predictions': ['id', 'user_id', 'cgpa', 'branch', 'internship_count', 'project_count', 
                           'certification_count', 'skill_count', 'placement_probability', 'expected_salary', 
                           'risk_level', 'prediction_date'],
            'resume_data': ['id', 'user_id', 'file_name', 'file_path', 'extracted_text', 
                           'extracted_skills', 'upload_date'],
            'skill_gaps': ['id', 'user_id', 'missing_skills', 'recommendations', 'priority', 'analysis_date'],
            'simulations': ['id', 'user_id', 'original_probability', 'new_probability', 
                           'changes_made', 'simulation_date'],
            'admin_stats': ['id', 'total_students', 'avg_placement_probability', 'high_risk_count', 'updated_at']
        }
        
        all_ok = True
        
        for table_name, expected_columns in expected_tables.items():
            cursor.execute(f"PRAGMA table_info({table_name})")
            actual_columns = [column[1] for column in cursor.fetchall()]
            
            print(f"Table: {table_name}")
            print(f"  Expected columns: {len(expected_columns)}")
            print(f"  Actual columns: {len(actual_columns)}")
            
            missing = set(expected_columns) - set(actual_columns)
            extra = set(actual_columns) - set(expected_columns)
            
            if missing:
                print(f"  ❌ Missing columns: {missing}")
                all_ok = False
            if extra:
                print(f"  ℹ️  Extra columns: {extra}")
            if not missing and not extra:
                print(f"  ✓ Schema correct!")
            
            print()
        
        conn.close()
        
        if all_ok:
            print("✅ All tables verified successfully!")
        else:
            print("❌ Some issues found. Run migrate_db.py to fix.")
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    verify_database()
