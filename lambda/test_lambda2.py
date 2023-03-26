import boto3
import botocore
import pytest
from moto import mock_dynamodb
import unittest
from unittest import mock
from boto3.dynamodb.conditions import Key
import json
import os

import visitcount


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@mock_dynamodb
class TestHandlerCase(unittest.TestCase):
    def setUp(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.count_table = self.dynamodb.create_table(
            TableName='cloud-resume-challenge',
            KeySchema=[
                {
                    'AttributeName': 'ID',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'ID',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        self.count_table.put_item(
            Item={
                'ID': 'VISITOR_COUNT',
                'visitor_count': 0
            }
        )

    def test_get_item(self):
        event = {}
        context = {}
        response = visitcount.lambda_handler(event, context)

        self.assertTrue(response['statusCode'], 200)
        self.assertTrue(response["body"], '{"count": "\\"0\\""}')

    def test_put_item(self):
        event = {}
        context = {}
        response = visitcount.lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 200)


if __name__ == '__main__':
    unittest.main()