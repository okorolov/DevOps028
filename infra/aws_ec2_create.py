#!/usr/bin/python3
import boto3

# UserData option, those commands will start at the beginning of the create instance
user_data = '''#!/bin/bash
export BUILD_NAME={0}
aws s3 cp s3://samsara-infrastructure/first_run.sh .
chmod +x ./first_run.sh
./first_run.sh
'''


# Function for creating new instance
def aws_create_instance(event, context):
    # Get filename of the newly created build uploaded to S3 bucket
    filename = event['Records'][0]['s3']['object']['key']
    ec2 = boto3.resource('ec2')
    # Delete all existing instances with Samsara
    for instance in ec2.instances.all():
        for tag in instance.tags:
            if tag['Value'] == 'EC2_Docker_Samsara':
                ec2.instances.filter(InstanceIds=[instance.id]).terminate()
    # Create new instance
    instances = ec2.create_instances(
        ImageId='ami-ebd02392',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        Placement={'AvailabilityZone': 'eu-west-1a'},
        TagSpecifications=[{'ResourceType': 'instance',
                            'Tags': [{'Key': 'Name', 'Value': 'EC2_Docker_Samsara'}]}],
        UserData=user_data.format(filename),
        IamInstanceProfile={'Name': 'EC2'},
        SecurityGroupIds=['sg-a7214adf'],
        KeyName='ec2-samsara-key'
    )
    # Wait until EC2 instance is up and retrieve the public dns name
    instance = instances[0]
    instance.wait_until_running()
    instance.load()
    send_new_samsara_ip(instance.public_dns_name)


# Function to send mail with new Public IP of EC instance
def send_new_samsara_ip(new_samsara_ip):
    to_email = "xalberg@gmail.com"
    from_email = "oleksii.korolov@protonmail.com"
    reply_to = "oleksii.korolov@protonmail.com"
    subject = "Samsara new IP"
    message = str(new_samsara_ip) + ":9000"
    client = boto3.client('ses')
    response = client.send_email(
        Source=from_email,
        Destination={'ToAddresses': [to_email]},
        Message={'Subject': {'Data': subject, 'Charset': 'utf8'},
                 'Body': {'Text': {'Data': message, 'Charset': 'utf8'}}},
        ReplyToAddresses=[reply_to]
    )
    print(response['MessageId'])
