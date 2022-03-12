import json
import os

import boto3


def lambda_handler(event, context):
    """Krcmaric API Entrypoint

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    client = boto3.client('dynamodb')
    response = client.update_item(
        TableName=os.getenv('COUNTER_TABLE'),
        Key={
            'id': {
                'S': 'counter'
            }
        },
        ReturnValues='UPDATED_NEW',
        UpdateExpression='SET #V = if_not_exists(#V, :start) + :inc',
        ExpressionAttributeNames={
            '#V': 'value'
        },
        ExpressionAttributeValues={
            ':start': {
                'N': '0'
            },
            ':inc': {
                'N': '1'
            }
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps(int(response['Attributes']['value']['N'])),
    }
