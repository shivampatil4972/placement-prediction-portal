"""
Clear all data from database tables
Keeps the schema intact but deletes all records
"""

import sqlite3

def clear_all_data():
    """Clear all data from all tables"""
    conn = sqlite3.connect('placement_portal.db')
    cursor = conn.cursor()
    
    print("Clearing all data from database...\n")
    
    # List of tables to clear (in order to avoid foreign key issues)
    tables = [
        'simulations',
        'skill_gaps',
        'resume_data',
        'predictions',
        'student_profiles',
        'admin_stats',
        'users'
    ]
    
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        
        if count > 0:
            cursor.execute(f'DELETE FROM {table}')
            print(f"✓ Deleted {count} records from '{table}'")
        else:
            print(f"  '{table}' was already empty")
    
    conn.commit()
    
    # Reset autoincrement counters
    cursor.execute("DELETE FROM sqlite_sequence")
    conn.commit()
    
    print("\n✓ All data cleared successfully!")
    print("✓ Auto-increment counters reset")
    print("\nYou can now register a new account and start fresh.")
    
    conn.close()

if __name__ == '__main__':
    response = input("This will DELETE ALL DATA from the database. Are you sure? (yes/no): ")
    if response.lower() == 'yes':
        clear_all_data()
    else:
        print("Operation cancelled.")
