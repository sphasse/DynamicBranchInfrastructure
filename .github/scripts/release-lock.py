#!/usr/bin/env python3

import argparse
import sys
from python_dynamodb_lock.python_dynamodb_lock import *
import boto3
import logging

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

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

dynamodb_resource = boto3.resource('dynamodb', region_name=args.region)
lock_client = DynamoDBLockClient(dynamodb_resource, table_name=args.table)
# uses an internal method to look up an existing lock from the database
# and then reconstitutes a closeable lock from that information
db_lock = lock_client._get_lock_from_dynamodb(args.lock, '-')
new_lock = DynamoDBLock(
    partition_key=db_lock.partition_key,
    sort_key=db_lock.sort_key,
    owner_name=db_lock.owner_name,
    lease_duration=db_lock.lease_duration,
    record_version_number=db_lock.record_version_number,
    expiry_time=db_lock.expiry_time,
    additional_attributes=None,
    app_callback=None,
    lock_client=lock_client,
)
# enable the current lock_client to think it created this lock
new_lock.status=DynamoDBLock.LOCKED
lock_client._locks[new_lock.unique_identifier] = new_lock

#lock_client.release_lock(new_lock, best_effort=True)
lock_client.release_lock(new_lock)
print("Lock successfully released:")
print(new_lock)
lock_client.close()
