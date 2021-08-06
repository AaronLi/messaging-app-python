import hashlib

import boto3

from settings import MAILBOXES_TABLE_NAME, RECEIVE_CODE_ENCODING

dynamodb = boto3.client('dynamodb')

def decode_message(raw_message_map):
    message_map = raw_message_map['M']

    return {
        'from': message_map['from']['S'],
        'text': message_map['text']['S']
    }

def handle_acknowledge(event, context):
    mailbox_id = event.get('box')
    receive_code_raw = event.get('receive-code')

    missing_params = []

    if mailbox_id is None:
        missing_params.append('box')
    if receive_code_raw is None:
        missing_params.append('receive-code')

    if missing_params:
        raise Exception(f'Missing parameters {{{", ".join(missing_params)}}}')

    mailbox_retrieve = dynamodb.get_item(
        TableName=MAILBOXES_TABLE_NAME,
        Key={
            'receiveBox': {'S': mailbox_id}
        },
        ProjectionExpression='salt, receiveCodeHash, messages'
    ).get('Item')
    if not mailbox_retrieve:
        raise Exception('mailbox does not exist')

    salt = mailbox_retrieve.get('salt', '')['S']

    hasher = hashlib.sha256()

    hasher.update(receive_code_raw.encode(RECEIVE_CODE_ENCODING))
    hasher.update(salt.encode(RECEIVE_CODE_ENCODING))

    hashed_receive_code = hasher.hexdigest()

    if 'receiveCodeHash' not in mailbox_retrieve:
        raise Exception('Mailbox configuration error')

    correct_code = mailbox_retrieve['receiveCodeHash']['S']

    if hashed_receive_code == correct_code:
        dynamodb.update_item(
            TableName=MAILBOXES_TABLE_NAME,
            Key={
                'receiveBox': {'S': mailbox_id}
            },
            UpdateExpression='REMOVE messages[0]'
        )
        messages = mailbox_retrieve['messages']['L']
        if messages:
            del messages[0]

        if messages:
            return {
                "statusCode": 200,
                "body": {
                    'message_count': len(messages),
                    'message': decode_message(messages[0])
                }
            }
        else:
            return {
                "statusCode": 200,
                "body": {
                    'message_count': len(messages)
                }
            }
    else:
        raise Exception('Invalid receive code')
