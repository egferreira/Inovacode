from __future__ import print_function
import datetime
import pickle
import os.path
import timedelta
import pandas as pd 
import numpy as np
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
# subject = 'marchesan.gregory@gmail.com'

class GoogleCalendarApi(object):

    creds = None
    service = None
    subject = None

    def __init__(self, subject):
        self.subject = subject
        self.creds = None
        self.service = None
        self.subject = None
        self.setup()

    def setup(self):
        
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../config/token.pickle'):
            with open('../config/token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../config/credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../config/token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_next_events(self, last_day, number=100):
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=number, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        events_df = pd.DataFrame()
        events_df = events_df.append(events, ignore_index=True)
        events_df = events_df[['summary', 'start', 'end']]
        events_df['start'] = events_df['start'].apply(lambda x: x.get('dateTime'))
        events_df['start'] = pd.to_datetime(events_df['start'])
        events_df['end'] = events_df['end'].apply(lambda x: x.get('dateTime'))
        events_df['end'] = pd.to_datetime(events_df['end'])
        events_df = events_df[events_df["summary"]=="Work"]
        events_df = events_df[events_df['start'] < last_day.tz_localize('UTC')]


        return events_df
    
    def set_event(self, init_time, end_time, title, description):
        d = datetime.datetime.utcnow().date()
        tomorrow = datetime.datetime(d.year, d.month, d.day, 10)+datetime.timedelta(days=1)
        start = tomorrow.isoformat()
        end = (tomorrow + datetime.timedelta(hours=1)).isoformat()
        body={"summary": 'Hello there, Automating calendar', 
            "description": 'Google calendar with python',
            "start": {"dateTime": start, "timeZone": 'utc'}, 
            "end": {"dateTime": end, "timeZone": 'utc'},
            }

        event = self.service.events().insert(calendarId=self.subject,body=body).execute()

    def process_work_slices(events):
        


        pass
        # time_slices = pd.DataFrame(columns=['Summary', 'Init Time', 'End Time'])
        # for event in events:
        #     summary = event['summary']
        #     if(summary == "Work"):    
        #         start = event['start'].get('dateTime', event['start'].get('date'))
        #         end = event['end'].get('dateTime', event['end'].get('date'))
        #         line = {"Summary" : summary,
        #                 "Init Time" : start,
        #                 "End Time" : end
        #         }
        #         time_slices.append(line)
        
        # return time_slices

if __name__ == '__main__':
    # main()
    pass