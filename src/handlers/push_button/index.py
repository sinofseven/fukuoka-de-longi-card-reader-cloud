from jeffy.framework import Jeffy
from botocore.client import BaseClient
from boto3.dynamodb.table import TableResource

app = Jeffy()


@app.decorator.auto_logging
def handler(event, context):
    main(event)


def main(event: dict):
    if is_long_click(event):
        main_with_long(event)
    else:
        main_without_long(event)


def get_slack_bot_token(ssm_client: BaseClient):
    option = {
        'Name': '/CardReader/Application/SlackBotToken',
        'WithDecryption': True
    }
    resp = ssm_client.get_parameter(**option)
    return resp['Parameter']['Value']


def get_click_type(event: dict) -> str:
    return event['deviceEvent']['buttonClicked']['clickType']


def is_long_click(event: dict) -> bool:
    return get_click_type(event) == 'LONG'


def is_double_click(event: dict) -> bool:
    return get_click_type(event) == 'DOUBLE'


def main_with_long(event: dict):
    pass


def main_without_long(event: dict):
    times = 2 if is_double_click(event) else 1