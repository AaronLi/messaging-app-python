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

print(response.json()['body'])
