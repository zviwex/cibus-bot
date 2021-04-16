import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

my_config = Config(
    region_name='us-east-1',
)


def get_resource():
    return boto3.resource('dynamodb', config=my_config)


def put_user(userid, mail, password, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('accounts')
    response = table.put_item(
        Item={
            'userid': userid,
            'mail': mail,
            'password': password
        }
    )
    return response


def get_user(userid, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()
    table = dynamodb.Table('accounts')

    try:
        response = table.get_item(Key={'userid': userid})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        if 'Item' in response:
            return response['Item']

        raise Exception(f'user {userid} not exists')


def get_users(dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()
    table = dynamodb.Table('accounts')

    try:
        response = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']


def delete_user(userid, dynamodb=None):
    if not dynamodb:
        dynamodb = get_resource()

    table = dynamodb.Table('accounts')

    try:
        response = table.delete_item(
            Key={
                'userid': userid,
            },
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return response


if __name__ == '__main__':
    print(get_users())
    print(get_user('a'))
