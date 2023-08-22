from __future__ import print_function
from io import BytesIO

import gtts
from playsound import playsound

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        print(len(events))


        if not events:
            print('No upcoming events found.')
            return

        intro = gtts.gTTS("Hallo Micha, ich habe " + str(len(events)) + " Termine gefunden.", lang='de')
        filenameIntro = os.path.dirname(__file__) + '\\intro.mp3'
        intro.save(filenameIntro)
        playsound(filenameIntro)
        os.remove(filenameIntro)
        # Prints the start and name of the next 10 events
        for event in events:
            
            
            
            # You have to filter between date and datetime
            start = event['start'].get('dateTime', event['start'].get('date')) 
            if len(start) > 10:
                start = start[:-10]

            tts = gtts.gTTS(start + " " + event['summary'], lang='de')
            filename = os.path.dirname(__file__) + '\\abc.mp3'
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
            print(event['summary'])
            print(start)
            
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()