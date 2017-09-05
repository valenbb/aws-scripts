#!/usr/bin/env python

import boto3
import datetime

# Connection to resource
client = boto3.client('iam')

timeLimit=datetime.datetime.now() - datetime.timedelta(days=90)
timel=timeLimit.date()
mytime=timel.strftime('%m/%d/%Y')
print(mytime)

print("UserName;CreationDate,AccessKeyId,LastUsed...")

for user in client.list_users()['Users']:
    akey = client.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']

    username = user['UserName']

    for meta in akey:

      access_key = meta['AccessKeyId']

      last_access = client.get_access_key_last_used(AccessKeyId=meta['AccessKeyId'])['AccessKeyLastUsed']
      last_used = last_access['LastUsedDate'].date()
      last=last_used.strftime('%m/%d/%Y')
      #print(last)


      cdate = meta['CreateDate']
      keys_created=cdate.date()
      ckey=keys_created.strftime('%m/%d/%Y')
      #print(cdate)

      if keys_created >= timel:
         print ('%s;%s;%s;%s' % (username, ckey, access_key,last))