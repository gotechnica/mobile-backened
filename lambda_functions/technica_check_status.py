# Checks whether email and phone number is in DynamoDB
# Returns status 200 if the user is registered and in the database
# If not return a status 400
import base64
import os
import urllib
from urllib import request, parse
import boto3
import json
import random
from boto3.dynamodb.conditions import Key, Attr
import re
import time

TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('Technica-Data')
    response = table.scan(FilterExpression=Attr('phone').eq(event['phone']))
    
    if len(response[u'Items']) > 0:
        if event['phone'] == response[u'Items'][0][u'phone']:
            to_number = event['phone']
            from_number = os.environ.get("TWILIO_NUMBER")
            pin = random.randint(99999, 999999)
            print(pin)
            body = 'Your Technica pin verification code is: ' + str(pin)

            if not TWILIO_ACCOUNT_SID:
                return "Unable to access Twilio Account SID."
            elif not TWILIO_AUTH_TOKEN:
                return "Unable to access Twilio Auth Token."
            elif not to_number:
                return "The function needs a 'To' number."
            elif not from_number:
                return "The function needs a 'From'."
            elif not body:
                return "The function needs a 'Body' message to send."
                
            populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
            post_params = {"To": to_number, "From": from_number, "Body": body}
            
            data = parse.urlencode(post_params).encode()
            req = request.Request(populated_url)
            
            # add authentication header to request based on Account SID + Auth Token
            authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            base64string = base64.b64encode(authentication.encode('utf-8'))
            req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
        
            try:
                # perform HTTP POST request
                with request.urlopen(req, data) as f:
                    print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
            except Exception as e:
                print (e)
                # something went wrong!
                # return {"statusCode":400, "body": "Malformed number."}
                # Integration response in API gateway matches error message with regex and link it to specific HTTP status code
                raise Exception('Error. Invalid input: Malformed number.')

            
            response = table.update_item(
                Key={
                    'email': response[u'Items'][0][u'email']
                },
                UpdateExpression='SET expiration = :exp, pin = :pin',
                ExpressionAttributeValues={
                    ':pin': pin,
                    ':exp': int(time.time() + 300)
                }
            )
            
            return {"statusCode":200, "body": "SMS Successfully sent."}

        else:
            # return {"statusCode":400, "body": "Given number does not exist."}
            raise Exception('Error. Invalid input: Given number does not exist.')

    else:
        # return {"statusCode":400, "body": "Given number does not exist."}
        raise Exception('Error. Invalid input: Given number does not exist.')
