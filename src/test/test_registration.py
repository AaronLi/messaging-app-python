import json
import os
import argparse
import requests

parser = argparse.ArgumentParser()

parser.add_argument('--username', required=True)

args = parser.parse_args()

output_string = json.dumps({
        'username': args.username
    })

response = requests.post(
    'https://api.dumfing.com/messaging/messaging-app-register',
    headers={
        'x-api-key': os.environ['API_KEY'],
        'Content-Type': 'application/json'
    },
    data= output_string
)

try:
    if response.json()['statusCode'] != 200:
        raise Exception(f'Test failed {response.json()}')
    else:
        print(response.json())
except:
    raise Exception(f'Test failed {response.content}')