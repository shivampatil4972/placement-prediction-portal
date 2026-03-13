import sqlite3

conn = sqlite3.connect('placement_portal.db')
conn.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
cursor = conn.cursor()

# Check trends data
cursor.execute('''
    SELECT 
        DATE(prediction_date) as date,
        placement_probability,
        expected_salary
    FROM predictions
    WHERE user_id = 1
    ORDER BY prediction_date ASC
''')

trends = cursor.fetchall()
print(f'Prediction trends data ({len(trends)} records):')
for trend in trends:
    print(f'  {trend}')

# Check what the API should return
if trends:
    labels = [str(t['date']) for t in trends]
    probability = [float(t['placement_probability']) for t in trends]
    salary = [float(t['expected_salary']) for t in trends]
    
    print(f'\nAPI Response format:')
    print(f'  labels: {labels}')
    print(f'  probability: {probability}')
    print(f'  salary: {salary}')

conn.close()
