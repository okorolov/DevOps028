#!/usr/bin/python3
import boto3
import time

print('Loading function')

balancer = boto3.client('elb', region_name='eu-west-1')

def lb_create():
    # Create new Autoscaling Group
    samsara_lb = balancer.create_load_balancer(
        LoadBalancerName='samsara-lb',
        Listeners=[{'Protocol':'HTTP',
                    'LoadBalancerPort':80,
                    'InstanceProtocol':'HTTP',
                    'InstancePort':9000}],
        Subnets=['subnet-9cb528d5', 'subnet-e4d607bf'],
        SecurityGroups=['sg-a7214adf']
    )
    response = balancer.configure_health_check(
        LoadBalancerName='samsara-lb',
        HealthCheck={
            'Target': 'TCP:9000',
            'Interval': 5,
            'Timeout': 2,
            'UnhealthyThreshold': 5,
            'HealthyThreshold': 2
        }
    )
    print(samsara_lb)
    print(response)
lb_create()