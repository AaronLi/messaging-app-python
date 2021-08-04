import boto3

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

    if not dynamodb.get_item(TableName='mailboxes', Key={'receiveBox': {'S': receiver}}).get('Item'):
        raise Exception(f'Invalid mailbox {receiver}')

    dynamodb.update_item(
        TableName='mailboxes',
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
