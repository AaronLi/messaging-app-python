import json

import requests

from secrets import api_key, test_send_to, test_receive_code

response = requests.post(
    'https://api.dumfing.com/messaging/messaging-app-receive',
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

print(response.json()['body'])
