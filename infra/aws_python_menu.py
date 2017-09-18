#!/usr/bin/python3
import boto3
from botocore.exceptions import ClientError

# Function to check status of all instances
def aws_status():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()['Reservations']
    for lvldown in response:
        for each in lvldown['Instances']:
             for i in each.items():
                 if (
			'InstanceId' in i or
			'PrivateDnsName' in i or
			'PrivateIpAddress' in i or
			'State' in i or
			'VirtualizationType' in i or
			'ImageId' in i or
			'Architecture' in i or
			'Hypervisor' in i or
			'RootDeviceName' in i or
			'InstanceType' in i
		    ):
                     print(i)

# Function to start an aws instance
def aws_start():
    print('Enter instance id')
    instance_id = input()
    ec2 = boto3.client('ec2')
    # Do a dryrun to verify permissions
    try:
        ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    # Dry run succeeded, run start_instances without dryrun
    try:
        response = ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

# Function to start an aws instance
def aws_stop():
    print('Enter instance id')
    instance_id = input()
    ec2 = boto3.client('ec2')
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

# Function to restart an aws instance
def aws_restart():
    print('Enter instance id')
    instance_id = input()
    ec2 = boto3.client('ec2')
    # Do a dryrun first to verify permissions
    try:
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)

# Function to create an aws instance
# This will create only Ubuntu 16 t2.micro image and start it
def aws_create_instance():
    ec2 = boto3.resource('ec2')
    # Do a dryrun first to verify permissions
    try:
        ec2.create_instances(ImageId='ami-785db401', InstanceType='t2.micro', MaxCount=1, MinCount=1, DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise
    # If DryRun succeeded run creation of an instance
    try:
        instance = ec2.create_instances(ImageId='ami-785db401', InstanceType='t2.micro', MaxCount=1, MinCount=1)
        print(instance)
    except ClientError as e:
        print(e)

# Function for menu
def menu():
    while True:
        print('1. Get information about instances')
        print('2. Start instance')
        print('3. Stop instance')
        print('4. Restart instance')
        print('5. Create new instance')
        print('6. Quit')
        reply = int(input())

        if reply == 1:
            aws_status()
        elif reply == 2:
            aws_start()
        elif reply == 3:
            aws_stop()
        elif reply == 4:
            aws_restart()
        elif reply == 5:
            aws_create_instance()
        elif reply == 6:
            break
        else:
             print('pew')

print('Welcome to Amazon Control')
print('Select action:')

menu()
