#!/usr/bin/python3
import boto3

print('Loading function')

autoscaling = boto3.client('autoscaling', region_name='eu-west-1')

def as_create():
    # Try to delete an existing Autoscaling Group
    print('Deleting OLD Load Balancer, please wait...')
    try:
        autoscaling.delete_auto_scaling_group(AutoScalingGroupName='samsara-as', ForceDelete=True)
    except:
        pass
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