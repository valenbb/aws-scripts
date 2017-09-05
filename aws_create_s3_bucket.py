#!/usr/bin/env python

import boto3
import datetime
import json
import argparse

# Connection to resource
s3 = boto3.client('s3')

# Passing needed parameters
parser = argparse.ArgumentParser(description='Bucket creation and policy addtion')
parser.add_argument('bucket_name', help='name for S3 bucket to be created')
parser.add_argument('account', help='AWS account')
parser.add_argument('role_name', help='name for AWS role to use as Principal')

args = parser.parse_args()

# Set bucket name to variable
bucket_name = args.bucket_name
print(bucket_name)

# Set bucket name to variable
account = args.account
print(account)

# Set role name to variable
role_name = args.role_name
print(role_name)

# Create bucket using variable
print('\nCreating new bucket with name:%s.' % bucket_name)
response = s3.create_bucket(Bucket=bucket_name)
print (response)

# bucket policy
policy = {
        "Version": "2012-10-17",
        "Statement": [{
                        "Sid": "AddPerms",
                        "Effect": "Allow",
                        "Principal": {"AWS": ["arn:aws:iam::%s:role/%s" % (account, role_name)]},
                        "Action": ["s3:DeleteBucket", "s3:ListBucket"],
                        "Resource": "arn:aws:s3:::%s" % bucket_name
                },
                {
                        "Sid": "S3ObjectActions",
                        "Effect": "Allow",
                        "Principal": {"AWS": ["arn:aws:iam::%s:role/%s" % (account, role_name)]},
                        "Action": ["s3:DeleteObject", "s3:GetObject", "s3:PutObjectACL", "s3:PutObject"],
                        "Resource": "arn:aws:s3:::%s/*" % bucket_name
                }
        ]
}
# Convert the policy to a JSON string
bucket_policy = json.dumps(policy)

# Set the new policy on the given bucket
print('\nAdding bucket policy to bucket:%s.' % bucket_name)
response2 = s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
print(response2)