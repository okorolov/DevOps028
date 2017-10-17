#!/usr/bin/python3
import boto3
import time

print('Loading function')

autoscaling = boto3.client('autoscaling', region_name='eu-west-1')

def as_create():
    print('Creating new Autoscaling Group')
    # Create new Auto Scaling Group
    samsara_as = autoscaling.create_auto_scaling_group(
        AutoScalingGroupName='samsara-as',
        LaunchConfigurationName='samsara-lg',
        LoadBalancerNames=['samsara-lb'],
        HealthCheckType='ELB',
        HealthCheckGracePeriod=300,
        MinSize=1,
        MaxSize=3,
        DesiredCapacity=2,
        AvailabilityZones=['eu-west-1a']
    )
    print(samsara_as)

as_create()