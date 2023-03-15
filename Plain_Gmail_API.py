from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def GmailCredsCheck():
    #Credentials Check had to copy this from the sample code because could not get the Gmail API to accept the creds no other way
    creds = None
    if os.path.exists('/Users/kille/Project1_Networking/token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('/Users/kille/Project1_Networking/token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service
    
#Make the Email 
def GmailCreation(service):
    body = 'cs4390 Task 3a, Successful'
    mMessage = MIMEMultipart()
    mMessage['to'] = 'mtatarowicz21@gmail.com'
    mMessage['from'] = 'cs4390bg@gmail.com'
    mMessage['subject'] = 'Task 3 Plain Email'
    mMessage.attach(MIMEText(body, 'plain'))
    encode = base64.urlsafe_b64encode(mMessage.as_bytes()).decode()
    message = service.users().messages().send(userId='me', body={'raw': encode}).execute()
    print(message)
    
def main():
    service = GmailCredsCheck()
    GmailCreation(service)
    
    
if __name__ == '__main__':
    main()
