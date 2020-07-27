#!/usr/bin/env python3

import argparse
import sys
from python_dynamodb_lock.python_dynamodb_lock import *
import boto3

parser = argparse.ArgumentParser()
parser.add_argument("--table", help="The name of the DynamoDB lock table")
parser.add_argument("--region", help="The AWS region of the lock table")
args = parser.parse_args()
if args.table is None:
    print("You must provide a table name")
    sys.exit(1)
if args.region is None:
    print("You must provide an AWS region")
    sys.exit(1)

print(args.table)

# Create the lock table with the given name and region
dynamodb_client = boto3.client('dynamodb', region_name=args.region)
dynamodb_resource = boto3.resource('dynamodb', region_name=args.region)
lock_client = DynamoDBLockClient(dynamodb_resource)
lock_client.create_dynamodb_table(dynamodb_client, table_name=args.table)
lock_client.close()
