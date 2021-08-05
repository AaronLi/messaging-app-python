import json

import requests

from secrets import api_key, test_send_to, test_send_from, test_receive_code

response = requests.post(
    'https://40odyykuy0.execute-api.ca-central-1.amazonaws.com/default/messaging-app-acknowledge',
    headers={
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    },
    data=json.dumps(
        {
            'receive-code': test_receive_code,
            'box': test_send_to
        }
    )
)

print(response.json())
