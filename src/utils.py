from flask import jsonify, url_for
import hashlib
import os
from os.path import join, dirname, realpath
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from skpy import Skype

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
    body_plainText = MIMEText(body_receiver, "html")
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

# def longText(body):
#     textBody = """\
#         this is another test from python!
#         Interviewer: %s\r
#         Company Name: %s\r
#         Type: %s, %s\r
#         Live Coding: 
#         Interviewee: %s %s \r
#         Date/Time: %s \r
#         Job Title: %s \r
#         Job Description: \n %s \r
#     """%(body['InterviewerName'],body['Client'],body['Mode'],body['Type'],body['LiveCoding'],body['c_firstname'],body['c_lastname'],body['Time'],body['PositionTitle'],body['JD'])
#     return textBody

def googleCalendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    mycred = join(dirname(realpath(__file__)), "googleCalendar/mycredentials.json")
    mytoken = join(dirname(realpath(__file__)), "googleCalendar/token.json.json")
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(mycred, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(mytoken, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            return jsonify({
                "start": start,
                "summary": event['summary']
            })

    except HttpError as error:
        print('An error occurred: %s' % error)