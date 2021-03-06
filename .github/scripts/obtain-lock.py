#!/usr/bin/env python3

import argparse
import sys
from python_dynamodb_lock.python_dynamodb_lock import *
import boto3
import logging
from datetime import datetime, timedelta 

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

duration = timedelta(seconds=60)

parser = argparse.ArgumentParser()
parser.add_argument("--table", help="The name of the DynamoDB lock table")
parser.add_argument("--lock", help="The name of the lock to acquire")
parser.add_argument("--region", help="The AWS region of the lock table")
parser.add_argument("--duration", type=int, help="The duration of the lease in seconds (default: 60)")
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
if args.duration is not None:
    duration = timedelta(seconds=args.duration)

dynamodb_resource = boto3.resource('dynamodb', region_name=args.region)
lock_client = DynamoDBLockClient(dynamodb_resource, table_name=args.table, lease_duration=duration)
lock = lock_client.acquire_lock(args.lock)
print("Lock obtained successfully:")
print(lock)
lock_client.close()
