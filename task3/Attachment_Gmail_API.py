from __future__ import print_function
import os.path
from os.path import basename
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def GmailCredsCheck():
    #Credentials Check had to copy this from the sample code because could not get the Gmail API to accept the creds no other way
    creds = None
    #Change these to your own pathway
    if os.path.exists('/Users/kille/Project1_Networking/token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            #Change these to your own pathway
        with open('/Users/kille/Project1_Networking/token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service
    
#Make the Email 
def GmailCreation(service):
    body = 'cs4390 Task 3b, Successful'
    mMessage = MIMEMultipart()
    mMessage['to'] = 'mtatarowicz21@gmail.com'
    mMessage['subject'] = 'Task 3 Attachment Email'
    mMessage.attach(MIMEText(body, 'plain'))
    return mMessage
    
def GmailAttachment(service, mMessage):
  
    filename = "crime.pdf"
   #Opening the File and then attaching it to the message
    with open(filename, "rb") as attachment:
        file = MIMEApplication(
                attachment.read(),
                Name=basename(filename)
            )
        file['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
        mMessage.attach(file)
        text = mMessage.as_string()
    #Sending the Message through Gmail API        
    encode = base64.urlsafe_b64encode(mMessage.as_bytes()).decode()
    message = service.users().messages().send(userId='me', body={'raw': encode}).execute()
    print(message)

def main():
    service = GmailCredsCheck()
    message = GmailCreation(service)
    GmailAttachment(service, message)
    
if __name__ == '__main__':
    main()