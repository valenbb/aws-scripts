#!/usr/local/bin/python3

import boto3
import sys
import os
import json

client = boto3.client('ec2')

ec2instances = client.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        },
        {
            'Name': 'tag:Name',
            'Values': ['Docker-Swarm-Worker']
        }
    ])
# instantiate empty array
RunningInstances = []

for ec2res in ec2instances['Reservations']:
    for ec2ins in ec2res['Instances']:
        inst_id = "<InstanceId is undefined>"
        if 'InstanceId' in ec2ins:
            inst_id = ec2ins['InstanceId']
        RunningInstances.append(inst_id)
    
    print(inst_id + " " + "starting")
    client.start_instances(InstanceIds=[inst_id])
