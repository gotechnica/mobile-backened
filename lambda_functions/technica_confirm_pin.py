import random
import boto3
import time
from boto3.dynamodb.conditions import Key, Attr
import json

def lambda_handler(event, context):
    client = boto3.resource('dynamodb')
    table = client.Table('Technica-Data')
    response = table.scan(FilterExpression=Attr('phone').eq(event['phone']))
    print(event)
    if len(response[u'Items']) > 0:
        print(event['phone'] == response[u'Items'][0][u'phone'])
        if event['phone'] == response[u'Items'][0][u'phone'] and event['pin'] == str(response[u'Items'][0][u'pin']):
            expected_time = response[u'Items'][0][u'expiration']
            current_time = int(time.time())
            if current_time <= expected_time:
                data = {'user_data': {}}
                for item in response[u'Items'][0]:
                    if item == u'fav_events':
                        data['user_data']['fav_events'] = {}
                        for event in response[u'Items'][0][item]:
                            data['user_data']['fav_events'][str(event)] = True
                    elif item == u'minor_status':
                        data['user_data']['minor_status'] = response[u'Items'][0][item]
                    elif item == u'organizer':
                        data['user_data']['organizer'] = response[u'Items'][0][item]
                    elif item == u'dietary_restrictions':
                        data['user_data']['dietary_restrictions'] = []
                        for restriction in response[u'Items'][0][item]:
                            data['user_data']['dietary_restrictions'].append(str(restriction))
                    else:
                        data['user_data'][item] = str(response[u'Items'][0][item])
                print(data)
                return {"statusCode":200, "body": data}

    raise Exception('Error. Invalid input: pin is invalid.')
