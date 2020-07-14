import json
import boto3, os, time
import datetime

print('Loading function')

ddb_latest_episodes = os.environ['ddb_latest_episodes']
expiry_time = int(os.environ['expiry_time'])

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):


    # print("Received event: " + json.dumps(event, indent=2))
    # print(event)
    for record in event['Records']:
        print(record['eventID'])
        # print(record['eventName'])
        if 'INSERT' in record['eventName']:
            # print("DynamoDB Record: " + json.dumps(record['dynamodb']['NewImage'], indent=2))
            new_show_details = record['dynamodb']['NewImage']
            now = datetime.datetime.now()
            expiry_ttl = (now + datetime.timedelta(days=expiry_time)).timestamp()

            new_show_details.update(
                {
                    "expiry_ttl": {"S": str(expiry_ttl)}
                }
            )

            print(new_show_details)
            dynamodb.put_item(TableName=ddb_latest_episodes, Item=new_show_details)

        return 'Successfully processed {} records.'.format(len(event['Records']))
