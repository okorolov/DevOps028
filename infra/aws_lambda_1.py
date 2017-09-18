#!/usr/bin/python3
import boto3
import time
from botocore.exceptions import ClientError

# UserData option, those commands will start at the beginning of the create instance
userdata = '''#!/bin/bash
export DB_HOST={0}
aws s3 cp s3://samsara-infrastructure/first_run_ec2.sh .
chomd +x first_run.sh
./first_run.sh
'''


# Function for creating new instance
def aws_create_instance(event, context):
    rds = boto3.client('rds')
    running = True
    while running:
        response = rds.describe_db_instances(DBInstanceIdentifier=db_identifier)
        db_instances = response['DBInstances']
        db_instance = db_instances[0]
        status = db_instance['DBInstanceStatus']
        time.sleep(5)
        if status == 'available':
            endpoint = db_instance['Endpoint']
            host = endpoint['Address']
            # port = endpoint['Port']
            running = False
    ec2 = boto3.resource('ec2')
    try:
        instance = ec2.create_instances(
            ImageId='ami-ebd02392',  # Amazon Linux image
            InstanceType='t2.micro',  # Instance Type
            MaxCount=1,  # The maximum number of instances to launch
            MinCount=1,  # The minimum number of instances to launch
            # Name Tag for the instance
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'EC2_Docker_Samsara'}]}],
            UserData=userdata.format(host),  # Set of commands to run when the new isnatance is created
            IamInstanceProfile={'Name': 'EC2'},  # IAM profile name
            SecurityGroupIds=['sg-a7214adf'],  # Network security group
            KeyName='ec2-samsara-key'  # Assigning a keypair
        )
        print(instance)
    except ClientError as e:
        print(e)


