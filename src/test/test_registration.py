import json

import requests

from secrets import api_key, test_send_from

output_string = json.dumps({
        'username': test_send_from
    })

response = requests.post(
    'https://api.dumfing.com/messaging/messaging-app-register',
    headers={
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    },
    data= output_string
)

if response.json()['statusCode'] != 200:
    raise Exception(f'Test failed {response.json()}')
else:
    print(response.json())