import boto3
import json

# Checks whether email and phone number is in DynamoDB
# Returns status 200 if the user is registered and in the database
# If not returns a status 400

def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    response = client.get_item(TableName='Technica-Data',Key={'email':{'S':event['email']}})
    
    if 'Item' in response:
        if event['phone'] == response['Item']['phone']['S']:
            return {"statusCode": 200, \
                    "headers": {"Content-Type": "application/json"}, \
                    "body": response}
        else:
            raise Exception('Invalid input: Phone number not found.')
    else:
        raise Exception('Invalid input: Email not found.')
        