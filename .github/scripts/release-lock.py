#!/usr/bin/env python3

import argparse
import sys
from python_dynamodb_lock.python_dynamodb_lock import *
import boto3

parser = argparse.ArgumentParser()
parser.add_argument("--table", help="The name of the DynamoDB lock table")
parser.add_argument("--lock", help="The name of the lock to acquire")
parser.add_argument("--region", help="The AWS region of the lock table")
args = parser.parse_args()
if args.table is None:
    print("You must provide a table name")
    sys.exit(1)
if args.lock is None:
    print("You must provide a lock name")
    sys.exit(1)
if args.region is None:
    print("You must provide an AWS region")
    sys.exit(1)

print(args.table)

# get a reference to the DynamoDB resource
dynamodb_resource = boto3.resource('dynamodb', region_name=args.region)
lock_client = DynamoDBLockClient(dynamodb_resource, table_name=args.table)
lock = lock_client._get_lock_from_dynamodb(args.lock, '-')
print(lock)

new_lock = DynamoDBLock(
    partition_key=lock.partition_key,
    sort_key=lock.sort_key,
    owner_name=lock.owner_name,
    lease_duration=lock.lease_duration,
    record_version_number=lock.record_version_number,
    expiry_time=lock.expiry_time,
    additional_attributes=None,
    app_callback=None,
    lock_client=lock_client,
)
lock_client.release_lock(new_lock)
lock_client.close()
