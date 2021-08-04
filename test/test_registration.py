import requests

from secrets import api_key

response = requests.put(
    'https://40odyykuy0.execute-api.ca-central-1.amazonaws.com/default/messaging-app-register',
    headers={
        'x-api-key': api_key
    },
    username='tester'
)

print(response.json(), response.headers)