"""
Migration script to fix database schema issues
"""
import sqlite3

DB_FILE = 'placement_portal.db'

def migrate():
    """Fix database schema - add missing columns with correct names"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        print("Checking and fixing database schema...")
        
        # Fix users table
        cursor.execute("PRAGMA table_info(users)")
        users_columns = [column[1] for column in cursor.fetchall()]
        
        if 'last_login' not in users_columns:
            print("  - Adding last_login to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN last_login TIMESTAMP")
        
        # Fix student_profiles table
        cursor.execute("PRAGMA table_info(student_profiles)")
        profiles_columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_at' not in profiles_columns:
            print("  - Adding created_at to student_profiles...")
            cursor.execute("ALTER TABLE student_profiles ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        if 'updated_at' not in profiles_columns:
            print("  - Adding updated_at to student_profiles...")
            cursor.execute("ALTER TABLE student_profiles ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        # Fix predictions table - uses prediction_date not created_at
        cursor.execute("PRAGMA table_info(predictions)")
        predictions_columns = [column[1] for column in cursor.fetchall()]
        
        if 'prediction_date' not in predictions_columns:
            print("  - Adding prediction_date to predictions...")
            cursor.execute("ALTER TABLE predictions ADD COLUMN prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        # Fix resume_data table - uses upload_date not created_at
        cursor.execute("PRAGMA table_info(resume_data)")
        resume_columns = [column[1] for column in cursor.fetchall()]
        
        if 'upload_date' not in resume_columns:
            print("  - Adding upload_date to resume_data...")
            cursor.execute("ALTER TABLE resume_data ADD COLUMN upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        # Fix skill_gaps table - uses analysis_date not created_at
        cursor.execute("PRAGMA table_info(skill_gaps)")
        skill_gaps_columns = [column[1] for column in cursor.fetchall()]
        
        if 'analysis_date' not in skill_gaps_columns:
            print("  - Adding analysis_date to skill_gaps...")
            cursor.execute("ALTER TABLE skill_gaps ADD COLUMN analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        # Fix simulations table - uses simulation_date not created_at
        cursor.execute("PRAGMA table_info(simulations)")
        simulations_columns = [column[1] for column in cursor.fetchall()]
        
        if 'simulation_date' not in simulations_columns:
            print("  - Adding simulation_date to simulations...")
            cursor.execute("ALTER TABLE simulations ADD COLUMN simulation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        
        conn.commit()
        print("\n✓ Database schema fixed successfully!")
        conn.close()
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")

if __name__ == "__main__":
    migrate()
