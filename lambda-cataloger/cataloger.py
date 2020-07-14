import json
import boto3, os, time
import datetime

print('Loading function')

ddb_catalog_name = os.environ['ddb_catalog']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(ddb_catalog_name)

print('ddb_catalog: {}'.format(ddb_catalog_name))

def lambda_handler(event, context):
    # print("Event:", event)
    message = event['Records'][0]['Sns']['Message']
    # print("message type:", type(message))
    # print("S3 Event:",message)
    s3_event_message = json.loads(message)
    # print("S3 JSON Event:", s3_event_message)

    for record in s3_event_message['Records']:
        # print(record)

        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        size = record['s3']['object']['size']

        radiostation, showname, episode = key.split('/')

        # obtain episode timestamp details from filename
        episode_details = episode.split('-')
        # print (episode_details)
        episode_year = episode_details[2]
        episode_month = episode_details[3]
        episode_date_time = episode_details[4]

        # TODO: fix file name in Streamripper so that it's easier to split.  'RADIOSTATION_SHOWNAME_YYYY-MM-DD-DAY-HH-MM'
        episode_date_time_details = episode_date_time.split('_')
        # print (episode_date_time_details)
        episode_date = episode_date_time_details[0]
        episode_day = episode_date_time_details[1]

        # episode_created_date = "{}-{}-{} 00:00:00+00:00".format(episode_year,episode_month,episode_date)
        episode_created_timestamp = datetime.datetime(int(episode_year), int(episode_month), int(episode_date)).timestamp()
        # print(episode_created_date)

        show_details = {
                'show_name': showname,
                'show_time': int(episode_created_timestamp),
                'radio_station': radiostation,
                'show_key' : key,
                'size' : size
        }

        print("Show details:", show_details)

        table.put_item(
            Item=show_details
        )