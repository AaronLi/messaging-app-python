import hashlib
import json

import boto3

dynamodb = boto3.client('dynamodb')

def decode_message(raw_message_map):
    message_map = raw_message_map['M']

    return {
        'from': message_map['from']['S'],
        'text': message_map['text']['S']
    }
def handle_receive(event, context):
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
        TableName='mailboxes',
        Key={
            'receiveBox': {'S': mailbox_id}
        },
        ProjectionExpression='salt, messages[0], receiveCodeHash'
    ).get('Item')
    if not mailbox_retrieve:
        raise Exception('mailbox does not exist')

    salt = mailbox_retrieve.get('salt', '')['S']

    hasher = hashlib.sha256()

    hasher.update(receive_code_raw.encode('ascii'))
    hasher.update(salt.encode('ascii'))

    hashed_receive_code = hasher.hexdigest()

    if 'receiveCodeHash' not in mailbox_retrieve:
        raise Exception('Mailbox configuration error')

    correct_code = mailbox_retrieve['receiveCodeHash']['S']

    if hashed_receive_code == correct_code:
        if 'messages' in mailbox_retrieve:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message_count': len(mailbox_retrieve['messages']['L']),
                    'messages': list(map(decode_message, mailbox_retrieve['messages']['L']))
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({'message_count': 0})
            }
    else:
        raise Exception('Invalid receive code')