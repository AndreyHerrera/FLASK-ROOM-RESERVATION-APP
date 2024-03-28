from flask import jsonify, request
import boto3


def generate_dbclient():
    return boto3.client('dynamodb', region_name='us-east-1')


def generate_dbresource():
    return boto3.resource('dynamodb', region_name='us-east-1')
