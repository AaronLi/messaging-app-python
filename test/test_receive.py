import json

import requests

from secrets import api_key, test_send_to, test_send_from

response = requests.post(
    'https://40odyykuy0.execute-api.ca-central-1.amazonaws.com/default/messaging-app-receive',
    headers={
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    },
    data=json.dumps(
        {
            'receive-code': 'U8unMe4QyJNZpYphwBL28kK88dsbswWi',
            'box': 'GhYRsLmx'
        }
    )
)

print(response.json()['body'])
