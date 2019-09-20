import boto3
import os
import sys
import uuid
from PIL import Image
import PIL.Image
import json

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(resized_path)


def lambda_handler(event, context):
    print(json.dumps(event))
    for record in event['Records']:
        original_bucket = os.environ["ORIGINAL_BUCKET"]
        thumbnail_bucket = os.environ["THUMBNAIL_BUCKET"]
        key = record['s3']['object']['key']
        filename = key.split('/')[1]
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), filename)
        upload_path = '/tmp/resized-{}'.format(filename)
        original_table = dynamodb.Table(os.environ["ORIGINAL_DDB_TABLE"])
        s3url = "https://{0}.s3-ap-northeast-1.amazonaws.com/{1}".format(
            original_bucket,
            key)
        original_table.put_item(Item={'id': str(uuid.uuid4()), 's3url': s3url})

        thumbnail_table = dynamodb.Table(os.environ["THUMBNAIL_DDB_TABLE"])

        s3url = "https://{0}.s3-ap-northeast-1.amazonaws.com/{1}".format(
            thumbnail_bucket,
            key)
        s3_client.download_file(original_bucket, key, download_path)
        resize_image(download_path, upload_path)
        s3_client.upload_file(upload_path, thumbnail_bucket, key)
        thumbnail_table.put_item(
            Item={'id': str(uuid.uuid4()), 's3url': s3url})
