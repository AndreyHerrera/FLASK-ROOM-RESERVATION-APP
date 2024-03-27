from flask import jsonify, request
import boto3


def generate_dbclient():
    return boto3.client('dynamodb', region_name='us-west-2',
                        endpoint_url='http://localhost:8888')
