import json
import os
import requests


response = requests.post(
    'https://api.dumfing.com/messaging/messaging-app-acknowledge',
    headers={
        'x-api-key': os.environ['API_KEY'],
        'Content-Type': 'application/json'
    },
    data=json.dumps(
        {
            'receive-code': os.environ['RECEIVE_CODE'],
            'box': os.environ['RECEIVE_BOX']
        }
    )
)

if response.json()['statusCode'] != 200:
    raise Exception(f'Test failed {response.json()}')
else:
    print(response.json())