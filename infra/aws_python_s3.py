#!/usr/bin/python3
import boto3
from botocore.exceptions import ClientError


# Function to print out current files in s3 bucket

def aws_s3_files():
    bucket_name = 'okorolov'  # replace with your bucket name
    key = 'Oleksii_Korolov.jpg'  # replace with your object key

    s3 = boto3.resource('s3')

    try:
        s3.Bucket(bucket_name).download_file(key, 'my_local_image.jpg')
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


aws_s3_files()


def connection_try_s3():
    counter = 4 # amount of connection tries
    while counter!=0:
        try:
            aws_s3_files()
            print("File succesfully downloaded")
            break
        except:
            raise
            counter-=1
