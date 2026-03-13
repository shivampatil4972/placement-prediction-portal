"""
Check database schema
"""

import sqlite3

conn = sqlite3.connect('placement_portal.db')
cursor = conn.cursor()

# Get table structure
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='predictions'")
schema = cursor.fetchone()

if schema:
    print("Predictions Table Schema:")
    print("="*80)
    print(schema[0])
    print("="*80)
    
    # Get actual column names
    cursor.execute("PRAGMA table_info(predictions)")
    columns = cursor.fetchall()
    
    print("\nColumns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Get sample data
    print("\n" + "="*80)
    print("Sample Data (first 3 rows):")
    print("="*80)
    
    cursor.execute("SELECT * FROM predictions LIMIT 3")
    rows = cursor.fetchall()
    
    col_names = [col[1] for col in columns]
    print(" | ".join(col_names))
    print("-" * 80)
    for row in rows:
        print(" | ".join(str(val) for val in row))

conn.close()
