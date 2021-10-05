#!/usr/bin/env python
import time
import os
import sys
import datetime
import boto.ec2
import boto3
from datetime import datetime, timedelta, date
import requests

profile = sys.argv[1]
region = sys.argv[2]

session = boto3.Session(profile_name=profile)
client = session.client('ec2', region_name=region)
lb = session.client('elbv2', region_name=region)
sts = session.client('sts', region_name=region)
account_id = sts.get_caller_identity()["Account"]


NOWTIME = datetime.now().strftime('%Y%m%d')

def count_running():
    response = client.describe_instances(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['running']
            }, 
        ])

    total_instance = []
    for reservation in (response['Reservations']):
        for instance in reservation['Instances']:
            total_instance.append(instance['InstanceId'])
    return len(total_instance)

def count_stopped():
    response = client.describe_instances(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['stopped']
            }, 
        ])

    total_instance = []
    for reservation in (response['Reservations']):
        for instance in reservation['Instances']:
            total_instance.append(instance['InstanceId'])
    return len(total_instance)

def count_images():
    response = client.describe_images(
        Owners=[
            'self',
        ],
    )

    total_images = []
    for Images in (response['Images']):
        total_images.append(Images['ImageId'])
    return len(total_images)

def count_lb():
    
    response = lb.describe_load_balancers(
        PageSize=123
    )

    total_lb = []
    for lbs in (response['LoadBalancers']):
        total_lb.append(lbs['LoadBalancerArn'])
    return len(total_lb)


def count_snapshot():
    response = client.describe_snapshots(
        OwnerIds=[
        account_id,
        ],
    )
    total_snapshot = []
    for snapshot in (response['Snapshots']):
        total_snapshot.append(snapshot['SnapshotId'])
    return len(total_snapshot)


def run():
    countrunning = count_running()
    print('Total Instance is running = %s' % (countrunning))

    countstopped = count_stopped()
    print('Total Instance is stopped = %s' % (countstopped))

    countimages = count_images()
    print('Total AMIs = %s' % (countimages))

    countlbs = count_lb()
    print('Total Loadbalancers = %s' % (countlbs))

    countsnapshot = count_snapshot()
    print('Total Snapshots = %s' % (countsnapshot))

if __name__ == '__main__':
    run()
