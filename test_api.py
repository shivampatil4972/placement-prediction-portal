import sys
sys.path.append('.')

from models.prediction import Prediction

# Test the get_prediction_trends method
user_id = 1
trends = Prediction.get_prediction_trends(user_id)

print(f'Raw trends data from model:')
for trend in trends:
    print(f'  {trend}')
    
# Simulate what the API returns
if trends:
    result = {
        'labels': [str(d['date']) for d in trends],
        'probability': [float(d['placement_probability']) for d in trends],
        'salary': [float(d['expected_salary']) for d in trends]
    }
    print(f'\nAPI would return:')
    import json
    print(json.dumps(result, indent=2))
else:
    print('No trends data found!')
