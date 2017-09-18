#!/usr/bin/python3
import boto3
import time
from botocore.exceptions import ClientError

# UserData option, those commands will start at the beginning of the create instance
userdata = '''#!/bin/bash
cd /tmp
yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
yum install -y docker
/etc/init.d/docker start
docker pull centos
'''


# Function for creating new instance
def aws_create_instance():
    ec2 = boto3.resource('ec2')
    try:
        instance = ec2.create_instances(
            ImageId='ami-ebd02392',  # Amazon Linux image
            InstanceType='t2.micro',  # Instance Type
            MaxCount=1,  # The maximum number of instances to launch
            MinCount=1,  # The minimum number of instances to launch
            # Name Tag for the instance
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'EC2_Docker_Samsara'}]}],
            UserData=userdata,  # Set of commands to run when the new isnatance is created
            IamInstanceProfile={'Name': 'EC2'},  # IAM profile name
            SecurityGroupIds=['sg-a7214adf'],  # Network security group
            KeyName='ec2-samsara-key'  # Assigning a keypair
        )
        print(instance)
        # Wait 30 seconds after the instance is created. This is needed to verify that all services are normally started
        time.sleep(30)
        # Start the status function again to obtain the instance.id of the newly created instance
        aws_status()
    except ClientError as e:
        print(e)


# Initial function
# Function to check status of the needed instance and start it if needed
# If the instance Tag is not found - new instance will be created aws_create_instance function
def aws_status():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter()
    instanceid = ''
    counter = 0
    # Get all instances and parse through them. Looking for a EC2_Docker_Samsara TAG.
    # If the needed tag is found - increase the counter.
    # If counter is 0 at the end of the run - aws_create_instance is called to create a new instance
    for instance in instances:
        for each in instance.tags:
            if 'EC2_Docker_Samsara' in each.values():
                if instance.state['Name'] == 'running':
                    counter += 1
                    instanceid = instance.id
                elif instance.state['Name'] == 'terminated':
                    pass
                elif instance.state['Name'] == 'pending':
                    time.sleep(10)
                    counter += 1
                    instanceid = instance.id
                else:
                    instance.start()
                    instanceid = instance.id
                    counter += 1
                    print('Instance Started')
            else:
                pass
    if counter == 0:
        aws_create_instance()
    else:
        print(instanceid)
        aws_get_latest_s3_file(instanceid)


# Obtain the latest file from the bucket samsara-builds and put it into the EC2 instance
def aws_get_latest_s3_file(instanceid):
    s3 = boto3.client('s3')
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    objs = s3.list_objects_v2(Bucket='samsara-builds')['Contents']
    filename = [obj['Key'] for obj in sorted(objs, key=get_last_modified)][-1]
    instance_ids = [instanceid]
    aws = boto3.session.Session()
    reset_counter = 0
    # Try to send the command via the ssm. If fails - retry in 5 seconds for a total of 50 seconds
    while True:
        try:
            output = aws.client('ssm').send_command(
                InstanceIds=instance_ids,
                DocumentName='AWS-RunShellScript',
                Parameters={
                    "commands": [
                        "aws s3 cp s3://samsara-builds/" + str(filename) + " " + str(filename)
                    ],
                    "executionTimeout": ["3600"]
                }
            )
            print(output['Command']['CommandId'])
            break
        except:
            if reset_counter == 10:
                break
            else:
                reset_counter += 1
                time.sleep(5)
                print(reset_counter)
