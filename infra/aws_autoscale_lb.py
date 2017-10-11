#!/usr/bin/python3
import boto3

print('Loading function')

autoscaling = boto3.client('autoscaling', region_name='eu-west-1')
balancer = boto3.client('elb', region_name='eu-west-1')

def lb_create():
    # Try to delete an existing Load Balancer
    print('Deleting OLD Load Balancer, please wait...')
    try:
        autoscaling.delete_auto_scaling_group(AutoScalingGroupName='samsara-as', ForceDelete=True)
        balancer.delete_load_balancer(LoadBalancerName='samsara-lb')
    except:
        pass
    print('Creating new Load Balancer')
    # Create new Load Balancer
    samsara_lb = balancer.create_load_balancer(
        LoadBalancerName='samsara-lb',
        Listeners=[{'Protocol':'HTTP',
                    'LoadBalancerPort':80,
                    'InstanceProtocol':'HTTP',
                    'InstancePort':9000}],
        Subnets=['subnet-9cb528d5', 'subnet-e4d607bf'],
        SecurityGroups=['sg-a7214adf']
    )
    print(samsara_lb)

lb_create()