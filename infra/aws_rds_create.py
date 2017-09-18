#!/usr/bin/python3
import boto3
import re
import time

print('Loading function')

s3 = boto3.resource('s3')


# Connect to S3 bucket and get the body of liquibase.properties file
# Parse through liquibase.properties and take username, pass, and db name
# Call function to create RDS with found settings
def s3_get_properties(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    s3_file = s3.Object(bucket, key)
    file_body = str(s3_file.get()["Body"].read())
    db_username = (re.findall("username: \w*", file_body))[0].split(':')[1].strip()
    db_password = (re.findall("password: \w*", file_body))[0].split(':')[1].strip()
    db_name = (re.findall("5432/\w*", file_body))[0].split('/')[1].strip()
    rds_create(db_username, db_password, db_name)


# Creates RDS instance with the defined settings
def rds_create(db_username, db_password, db_name):
    rds = boto3.client('rds')
    # Try to delete an existing samsara rds
    try:
        rds.delete_db_instance(DBInstanceIdentifier='samsara-postgres', SkipFinalSnapshot=True)
    except:
        pass
    # Wait until instance is deleted
    running = True
    while running:
        response = rds.describe_db_instances()
        db_instances = response['DBInstances']
        if len(db_instances) == 0:
            running = False
        else:
            time.sleep(10)
    # Create new RDS instance
    samsara_db = rds.create_db_instance(
        Engine='postgres',
        DBInstanceClass='db.t2.micro',
        MultiAZ=False,
        StorageType='gp2',
        AllocatedStorage=5,
        DBInstanceIdentifier='samsara-postgres',
        DBName=db_name,
        MasterUsername=db_username,
        MasterUserPassword=db_password,
        StorageEncrypted=False,
        AutoMinorVersionUpgrade=True,
        VpcSecurityGroupIds=['sg-e7ffa69f'],
        AvailabilityZone='eu-west-1a',
        Tags=[{'Key': 'Name', 'Value': 'SamsaraBD'}]
    )
    print(samsara_db)
