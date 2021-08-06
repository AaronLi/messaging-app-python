import argparse
import json
import os
import requests

parser = argparse.ArgumentParser()

parser.add_argument('--sender', required=True)
parser.add_argument('--message', default='Hello!')

args = parser.parse_args()

response = requests.post(
    'https://api.dumfing.com/messaging/messaging-app-send',
    headers={
        'x-api-key': os.environ['API_KEY'],
        'Content-Type': 'application/json'
    },
    data=json.dumps(
        {
            "from": args.sender,
            "to_box": os.environ['RECEIVE_BOX'],
            'message': args.message
        }
    )
)

try:
    if response.json()['statusCode'] != 200:
        raise Exception(f'Test failed {response.json()}')
    else:
        print(response.json())
except:
    raise Exception(f'Test failed {response.content}')