import json

import requests

from secrets import api_key, test_send_to, test_send_from

response = requests.post(
    'https://api.dumfing.com/messaging/messaging-app-send',
    headers={
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    },
    data=json.dumps(
        {
            "from": test_send_from,
            "to_box": test_send_to,
            'message': 'Hello!'
        }
    )
)

if response.json()['statusCode'] != 200:
    raise Exception(f'Test failed {response.json()}')
else:
    print(response.json())
