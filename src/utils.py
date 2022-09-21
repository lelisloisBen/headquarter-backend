from flask import jsonify, url_for
import hashlib
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from skpy import Skype

# sending email from rackspace
emailSenderTest = os.environ.get('EMAIL_SENDER')
passwordSenderTest = os.environ.get('PASSWORD_SENDER')
# sending skype message
skypeUsername = os.environ.get('SKYPE_USERNAME')
skypePassword = os.environ.get('SKYPE_PASSWORD')
skypeChannelID = os.environ.get('SKYPE_CHANNEL_ID')


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def sha256(string):
    m = hashlib.sha256()
    m.update(string.encode('utf-8'))
    return m.hexdigest()

def sendEmail(receiver,subject,body):
    sender_email = emailSenderTest
    password = passwordSenderTest
    receiver_email = receiver
    subject_email = subject
    body_receiver = body

    message = MIMEMultipart("alternative")
    message["Subject"] = subject_email
    message["From"] = sender_email
    message["To"] = receiver_email
    body_plainText = MIMEText(body_receiver, "plain")
    message.attach(body_plainText)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("secure.emailsrvr.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def sendSkype(body):
    sk = Skype(skypeUsername,skypePassword) 
    channel = sk.chats.chat(skypeChannelID) 
    channel.sendMsg(body)