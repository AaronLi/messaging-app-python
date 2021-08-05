import json

import boto3
from string import ascii_lowercase, ascii_uppercase, digits
import random
import hashlib

from settings import USERS_TABLE_NAME, MAILBOXES_TABLE_NAME

dynamodb = boto3.client('dynamodb')


def random_string(length):
    out_string = ''
    for i in range(length):
        out_string += random.choice(ascii_uppercase + ascii_lowercase + digits)
    return out_string


def handle_registration(event, context):
    if 'username' not in event:
        raise Exception('No username provided')

    user_name = event['username']

    existing_user = dynamodb.get_item(
        TableName=USERS_TABLE_NAME,
        Key={
            'userId': {'S': user_name}
        }
    ).get('Item')

    if existing_user:
        raise Exception('username already exists')

    mailbox_id = random_string(8)

    while dynamodb.get_item(TableName=MAILBOXES_TABLE_NAME, Key={'receiveBox': {'S': mailbox_id}}).get('Item'):
        mailbox_id = random_string(8)

    hasher = hashlib.sha256()

    receive_code = random_string(32)

    salt = random_string(32)

    hasher.update(receive_code.encode('ascii'))

    hasher.update(salt.encode('ascii'))

    hashed_code = hasher.hexdigest()

    dynamodb.put_item(
        TableName=USERS_TABLE_NAME,
        Item={
            'userId': {'S': user_name},
            'mailboxId': {'S': mailbox_id},
        }
    )

    dynamodb.put_item(
        TableName=MAILBOXES_TABLE_NAME,
        Item={
            'receiveBox': {'S': mailbox_id},
            'messages': {'L': []},
            'receiveCodeHash': {'S': hashed_code},
            'salt': {'S': salt}
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps({
            'receiveCode': receive_code,
            'receiveBox': mailbox_id
        })
    }
