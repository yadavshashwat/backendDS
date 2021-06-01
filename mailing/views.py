from django.shortcuts import render

# import requests
# import urllib2
# import http.client
# import urllib

from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication



from mailing.emails import *

import boto3
from botocore.exceptions import ClientError

# AWS SES
aws_smtp_username= "AKIAZYWQSOEIMR7WSCIE"
aws_smtp_password= "BFXzmGXQ5Px82+L0zLQRiWHKB48O0WvcfnkTWCuDMy8W"
aws_smtp_server = "email-smtp.ap-south-1.amazonaws.com"
aws_smpt_port = 25




AWS_ACCESS_ID = "AKIAZYWQSOEIOPTT6P7U"
AWS_KEY= "FrwkweN3TwDrJNzfVPfQT0shiKKptJXXdpIEXsrm"



# def send_sms(number,message,sender = sender_1,promotional = False):
#     if sender == sender_1:
#         message = message.replace(" ", "+")
#         if promotional:
#             url = "https://mobilnxt.in/api/push?accesskey="+sender1_authkey+"&to="+number+"&text="+message+"&from="+ sender_id
#         else:
#             url = "https://mobilnxt.in/api/push?accesskey="+sender1_authkey+"&to="+number+"&text="+message+"&from="+ sender_id

#         urllib2.urlopen(url)


# def send_email(from_mail,to_mail,server=server1,content=""):
#     return content


def send_mail(server="aws_ses", subject=None,to_email=None,from_email=None,content=None,attachment1 = None,filename1 = "Attachment 1", attachment2= None, filename2 = "Attachment 2"):
    # toaddr = to_email
    msg = MIMEMultipart('mixed')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    print(1)
    if attachment1:
        part1 = MIMEApplication(open(attachment1, 'rb').read())
        part1.add_header('Content-Disposition', 'attachment', filename=filename1)
        msg.attach(part1)

    if attachment2:
        part2 = MIMEApplication(open(attachment2, 'rb').read())
        part2.add_header('Content-Disposition', 'attachment', filename=filename2)
        msg.attach(part2)
    print(2)
    script = MIMEText(content, 'html')
    msg.attach(script)
    print(3)
    if server == "aws_ses":
        print(4)
        server = smtplib.SMTP(aws_smtp_server, aws_smpt_port)
        server.starttls()
        server.login(aws_smtp_username, aws_smtp_password)
        text = msg.as_string()
        server.sendmail(aws_smtp_username, to_email, text)
        server.quit()
        print(5)

def send_aws_email(from_email,to_email, subject,content_html):
    print(1)
    smtphost = aws_smtp_server
    # Get the user name and password - from the IAM user that is created by SES.
    password = aws_smtp_password
    username = aws_smtp_username
    message = content_html
    msg = MIMEMultipart()
    msg['From'] = "The Decor Shop <" + from_email + ">"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))
    print(2)
    server = smtplib.SMTP(smtphost)
    print(3)
    server.starttls()
    print(4)
    server.login(username, password)
    print(5)
    response = server.sendmail(msg['From'], msg['To'], msg.as_string())
    print(response)
    server.quit()


def send_password_reset_email(name,email,secret_string,test=True):
    # print("j")
    # print(secret_string)
    link = ""
    if test:
        print("ooo")
        link = "http://localhost:3000/adminpanel/passreset/" + str(secret_string)
    else:
        link = "http://www.thedecorship.in/adminpanel/passreset/" + str(secret_string)
    print("k")
    html_email = send_reset_link_html(name,link)
    print("l")
    # send_mail(subject="Password Reset | TheDecorShop TestEngine",to_email=email,from_email="info@thedecorshop.in",content=html_email)    
    send_aws_email(from_email="info@thedecorshop.in",to_email=email,subject="Password Reset | TheDecorShop TestEngine",content_html=html_email)    






def send_aws_email2(from_email,to_email, subject,content_html,content_text):

    SENDER = "The Decor Shop <" + from_email + ">"
    RECIPIENT = to_email
    AWS_REGION = "ap-south-1"

    # The subject line for the email.
    SUBJECT = subject

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = content_text
                
    # The HTML body of the email.
    BODY_HTML = content_html        

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.

    session = boto3.Session(
            aws_access_key_id = AWS_ACCESS_ID,
            aws_secret_access_key = AWS_KEY,
    )
    ses = session.client('ses',region_name=AWS_REGION)

    # client = boto3.client('ses',region_name=AWS_REGION)



    # Try to send the email.
    try:
        #Provide the contents of the email.
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
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])



# # def send_email(email="y.shashwat@gmail.com"):

