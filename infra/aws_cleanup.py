#!/usr/bin/python3
import boto3

print('Loading function')

autoscaling = boto3.client('autoscaling', region_name='eu-west-1')
balancer = boto3.client('elb', region_name='eu-west-1')
rds = boto3.client('rds', region_name='eu-west-1')

def aws_cleanup():
    # Try to delete an existing Autoscaling Group
    print('Deleting OLD Infrastructure, please wait...')
    print('Deleting Autoscaling group')
    try:
        autoscaling.delete_auto_scaling_group(AutoScalingGroupName='samsara-as', ForceDelete=True)
    except:
        pass
    print('Deleting Load Balancer')
    try:
        balancer.delete_load_balancer(LoadBalancerName='samsara-lb')
    except:
        pass
    print('Deleting RDS')
    try:
        rds.delete_db_instance(DBInstanceIdentifier='samsara-postgres', SkipFinalSnapshot=True)
    except:
        pass
    print('Deleting Launch Configuration')
    try:
        autoscaling.delete_launch_configuration(LaunchConfigurationName='samsara-lg')
    except:
        pass

aws_cleanup()