from boto3 import resource
import time

# The boto3 dynamoDB resource
dynamodb_resource = resource('dynamodb',  region_name='eu-west-2')
table = dynamodb_resource.Table('dynamodb')

def create_table_commits():
    table = dynamodb_resource.create_table(
        TableName='terraform_commits',
        KeySchema=[
            {
                'AttributeName': 'commits',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'commits',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )


def read_table_commits():

    table = dynamodb_resource.Table('terraform_commits')
    response = table.scan('commits')

    return response


def add_item_commits(item_to_add):
    table = dynamodb_resource.Table('terraform_commits')
    response = table.put_item(Item={'commits': item_to_add})

    return response


def delete_item_commits(item_to_delete):
    table = dynamodb_resource.Table('terraform_commits')
    response = table.delete_item(Key={'commits': item_to_delete})

    return response

def create_table_pcid():
    table = dynamodb_resource.create_table(
        TableName='terraform_pcid',
        KeySchema=[
            {
                'AttributeName': 'pcid',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'pcid',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
def read_table_pcid():

    table = dynamodb_resource.Table('terraform_pcid')
    response = table.scan('pcid')

    return response


def add_item_pcid(item_to_add):
    table = dynamodb_resource.Table('terraform_pcid')
    response = table.put_item(Item={'pcid': item_to_add})

    return response


def delete_item_pcid(item_to_delete):
    table = dynamodb_resource.Table('terraform_pcid')
    response = table.delete_item(Key={'pcid': item_to_delete})

    return response



