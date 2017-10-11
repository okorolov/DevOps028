#!/usr/bin/python3
import boto3

user_data = '''#!/bin/bash
aws s3 --region=eu-west-1 cp s3://samsara-infrastructure/first_run.sh .
chmod +x ./first_run.sh
./first_run.sh'''

print('Loading function')

autoscaling = boto3.client('autoscaling', region_name='eu-west-1')

def lg_create():
    # Try to delete an existing Launch Configuration
    print('Deleting OLD Launch Group, please wait...')
    try:
        autoscaling.delete_auto_scaling_group(AutoScalingGroupName='samsara-as', ForceDelete=True)
        autoscaling.delete_launch_configuration(LaunchConfigurationName='samsara-lg')
    except:
        pass
    print('Creating new Launch Configuration')
    # Create new Launch Configuration
    samsara_lg = autoscaling.create_launch_configuration(
        LaunchConfigurationName='samsara-lg',
        ImageId='ami-ebd02392',
        KeyName='ec2-samsara-key',
        SecurityGroups=['sg-a7214adf'],
        IamInstanceProfile='EC2',
        UserData=user_data
    )
    print(samsara_lg)

lg_create()