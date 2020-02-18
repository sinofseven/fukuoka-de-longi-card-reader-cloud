import json
import os

import boto3
from botocore.client import BaseClient
from jeffy.framework import Jeffy

app = Jeffy()


@app.decorator.auto_logging
def handler(event, context):
    return main(event)


def main(event, sns_client: BaseClient = boto3.client("sns")):
    body = event["body"]
    channel_id = get_target_channel_id()
    if has_target_channel(body, channel_id):
        topic_arn = get_target_topic_arn()
        publish(body, topic_arn, sns_client)
    return create_response(event)


def get_target_channel_id() -> str:
    value = os.environ["TARGET_CHANNEL_ID"]
    app.logger.info({"target_channel_id": value})

    return value


def get_target_topic_arn() -> str:
    value = os.environ["TARGET_TOPIC_ARN"]
    app.logger.info({"sns_topic_arn": value})
    return value


def has_target_channel(body: str, target_channel_id: str) -> bool:
    return body.find(target_channel_id) > 0


def publish(body: str, topic_arn: str, sns_client: BaseClient):
    option = {"TopicArn": topic_arn, "Message": body}
    resp = sns_client.publish(**option)
    app.logger.info({"publish_response": resp})


def create_response(event: dict) -> dict:
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"challenge": json.loads(event["body"]).get("challenge")}),
    }
