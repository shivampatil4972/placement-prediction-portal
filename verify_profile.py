import sqlite3

conn = sqlite3.connect('placement_portal.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('SELECT * FROM student_profiles WHERE user_id = 1')
profile = cursor.fetchone()

if profile:
    print('Profile created successfully:')
    for key in profile.keys():
        print(f'  {key}: {profile[key]}')
else:
    print('No profile found for user_id = 1')

conn.close()
