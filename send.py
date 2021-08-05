import boto3

from settings import MAX_MESSAGE_LENGTH, MAILBOXES_TABLE_NAME

dynamodb = boto3.client('dynamodb')


def handle_send(event, context):
    sender = event.get('from')
    receiver = event.get('to_box')
    message = event.get('message')
    missing_params = []
    if sender is None:
        missing_params.append('from')
    if receiver is None:
        missing_params.append('to_box')
    if message is None:
        missing_params.append('message')

    if missing_params:
        raise Exception(f'Missing parameters: {{{", ".join(missing_params)}}}')

    if len(message) > MAX_MESSAGE_LENGTH:
        raise Exception("Message too long")

    if not dynamodb.get_item(TableName=MAILBOXES_TABLE_NAME, Key={'receiveBox': {'S': receiver}}).get('Item'):
        raise Exception(f'Invalid mailbox {receiver}')

    dynamodb.update_item(
        TableName=MAILBOXES_TABLE_NAME,
        Key={
            'receiveBox': {'S': receiver}
        },
        UpdateExpression='SET messages = list_append(messages, :i)',
        ExpressionAttributeValues={
            ':i': {
                'L': [
                    {
                        'M': {
                            'text': {'S': message},
                            'from': {'S': sender}
                        }
                    }
                ]
            }
        },
        ReturnValues='UPDATED_NEW'
    )
    return {
        'statusCode': 200
    }
