#!/usr/bin/python3
import boto3
import sys

def send_new_samsara_ip(new_samsara_ip):
    to_email = "xalberg@gmail.com"
    from_email = "oleksii.korolov@protonmail.com"
    reply_to = "oleksii.korolov@protonmail.com"
    subject = "Samsara new IP"
    message = "http://" + str(new_samsara_ip)
    client = boto3.client('ses')
    response = client.send_email(
        Source=from_email,
        Destination={'ToAddresses': [to_email]},
        Message={'Subject': {'Data': subject, 'Charset': 'utf8'},
                 'Body': {'Text': {'Data': message, 'Charset': 'utf8'}}},
        ReplyToAddresses=[reply_to]
    )
    print(response['MessageId'])

send_new_samsara_ip(str(sys.argv))