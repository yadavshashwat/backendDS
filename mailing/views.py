from django.shortcuts import render

from datetime import datetime


from backendDS.credentials import AWS_SES_ACCESS_KEY, AWS_SES_SECRET_KEY

from mailing.emails import *
import boto3
from botocore.exceptions import ClientError

# AWS SES

def send_aws_email(from_email,to_email, subject,content_html):
    
    SENDER = "The Decor Shop <" + from_email + ">"
    RECIPIENT = to_email
    AWS_REGION = "ap-south-1"
    SUBJECT = subject
    BODY_HTML = content_html        
    CHARSET = "UTF-8"
    session = boto3.Session(
            aws_access_key_id = AWS_SES_ACCESS_KEY,
            aws_secret_access_key = AWS_SES_SECRET_KEY,
    )
    ses = session.client('ses',region_name=AWS_REGION)
    out = False
    try:
        response = ses.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    }                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        out = False
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        out = True
    return out




def send_password_reset_email(name,email,secret_string,test=True):
    link = ""
    if test:
        link = "http://localhost:3000/adminpanel/passreset/" + str(secret_string)
    else:
        link = "http://vendor.thedecorshop.in/adminpanel/passreset/" + str(secret_string)
    html_email = send_reset_link_html(name,link)
    out = send_aws_email(from_email="info@thedecorshop.in",to_email=email,subject="Password Reset | TheDecorShop Admin",content_html=html_email)    
    return out






# # def send_email(email="y.shashwat@gmail.com"):

