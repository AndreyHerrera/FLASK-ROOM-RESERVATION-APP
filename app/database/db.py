import boto3

AWS_ACCESS_KEY_ID = "AKIAVRUVSABSPCP2O6BF"
AWS_SECRET_ACCESS_KEY = "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"


def generate_dbclient():
    return boto3.client('dynamodb',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name='us-east-1')


def generate_dbresource():
    return boto3.resource('dynamodb',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name='us-east-1')
