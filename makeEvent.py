import datetime
import os.path
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authorize():

  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    return creds


def createEventOnCalendar(start_time, end_time):
    creds = authorize()
    
    try:
        service = build("calendar", "v3", credentials=creds)

        start_time_string = start_time.strftime('%Y-%m-%dT%H:%M:%S-07:00')
        end_time_string = end_time.strftime('%Y-%m-%dT%H:%M:%S-07:00')
        print(start_time_string)
        print(end_time_string)
        event = {
        'summary': 'Coding session',
        
        'description': 'You used vs code',
        'start': {
            'dateTime': f'{start_time_string}',  # Set your desired date and time
            'timeZone': 'America/Los_Angeles',  # Set your desired timezone
        },
        'end': {
            'dateTime': f'{end_time_string}',  # Set your desired end time
            'timeZone': 'America/Los_Angeles',
        },
        }

        # Insert the event into the primary calendar
        event_result = service.events().insert(calendarId='primary', body=event).execute()

        # Print the event details
        print(f"Event created: {event_result.get('htmlLink')}")

    except HttpError as error:
        print(f"An error occurred: {error}")


