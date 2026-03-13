import sqlite3

conn = sqlite3.connect('placement_portal.db')
cursor = conn.cursor()

# Find users without profiles
cursor.execute('''
    SELECT u.id, u.email, u.full_name 
    FROM users u 
    LEFT JOIN student_profiles sp ON u.id = sp.user_id 
    WHERE sp.id IS NULL AND u.user_type = 'student'
''')

users = cursor.fetchall()
print(f'Users without profiles: {len(users)}')
for user in users:
    print(f'  - ID: {user[0]}, Email: {user[1]}, Name: {user[2]}')

# Create default profiles for these users
if users:
    print('\nCreating default profiles...')
    for user in users:
        cursor.execute('''
            INSERT INTO student_profiles 
            (user_id, branch, cgpa, internship_count, project_count, certification_count, skills, placement_target)
            VALUES (?, 'Computer Science', 0.0, 0, 0, 0, '', '')
        ''', (user[0],))
    conn.commit()
    print(f'Created {len(users)} default profiles')

conn.close()
