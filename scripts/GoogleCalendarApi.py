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
import pendulum

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
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=number, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        events_df = pd.DataFrame()
        events_df = events_df.append(events, ignore_index=True)
        events_df = events_df[['summary', 'start', 'end', 'id']]
        events_df['start'] = events_df['start'].apply(lambda x: x.get('dateTime'))
        events_df['start'] = pd.to_datetime(events_df['start'])
        events_df['end'] = events_df['end'].apply(lambda x: x.get('dateTime'))
        events_df['end'] = pd.to_datetime(events_df['end'])
        events_df = events_df[events_df["summary"]=="Work"]
        events_df = events_df[events_df['start'] < last_day.tz_localize('UTC')]

        return events_df

    def check_concluded_events_this_week(self):
        # Call the Calendar API
        week_init = pendulum.now().start_of('week')
        print(week_init)
        last_day = pd.to_datetime(pendulum.now().end_of('week'))
        events_result = self.service.events().list(calendarId='primary', timeMin=week_init,
                                            maxResults=100, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        events_df = pd.DataFrame()
        events_df = events_df.append(events, ignore_index=True)
        events_df = events_df[['summary', 'description', 'start', 'end', 'id']]
        events_df['start'] = events_df['start'].apply(lambda x: x.get('dateTime'))
        events_df['start'] = pd.to_datetime(events_df['start'])
        events_df['end'] = events_df['end'].apply(lambda x: x.get('dateTime'))
        events_df['end'] = pd.to_datetime(events_df['end'])
        events_df = events_df[events_df['start'] < last_day.tz_localize('UTC')]
        events_df = events_df[events_df['description'].str.contains('DONE')]
        
        return events_df

        
    
    def set_event(self, init_time, end_time, title, description):
        start = init_time.to_pydatetime().isoformat()
        end = end_time.to_pydatetime().isoformat()
        body={"summary": title, 
            "description": 'Cardeal Assist',
            "start": {"dateTime": start, "timeZone": 'utc'}, 
            "end": {"dateTime": end, "timeZone": 'utc'},
            }

        event = self.service.events().insert(calendarId=self.subject,body=body).execute()

    def delete_events(self, eventsIds):
        for eventId in eventsIds:
            self.delete_event(eventId)

    def delete_event(self, eventId):
        event = self.service.events().delete(calendarId=self.subject,eventId=eventId).execute()

    def schedule_time(self, tasks, periods_df, pomodoro_break=pd.Timedelta(minutes=5)):
        periods_df["Total time"] = periods_df['end'] - periods_df['start']
        tasks['Time'] = tasks['Time'].apply(lambda x: pd.Timedelta(minutes=x))
        tasks.sort_values(by=["Priority", "Time"], ascending=False, inplace=True)

        tasks_processing = tasks.copy()
        
        # scheduled_tasks = pd.DataFrame("Summary", "Init Time", "End Time")
        for task in range(0, len(tasks_processing)):
            # pomodoro_time = pd.Timedelta(minutes=((tasks_processing.iloc[task, tasks_processing.columns.get_loc("Time")]/25)-1)*pomodoro_break)
            pomodoro_time = pd.Timedelta(minutes=0)
            for time_slice in range(0, len(periods_df)):
                if(periods_df.iloc[time_slice, periods_df.columns.get_loc('end')] == periods_df.iloc[time_slice, periods_df.columns.get_loc('start')]):
                    continue

                elif(tasks_processing.iloc[task, tasks_processing.columns.get_loc("Time")] + pomodoro_time < periods_df.iloc[time_slice, periods_df.columns.get_loc('Total time')]):
                    summary = tasks_processing.iloc[task, tasks_processing.columns.get_loc('Task')]
                    start = periods_df.iloc[time_slice, periods_df.columns.get_loc('start')]
                    end = periods_df.iloc[time_slice, periods_df.columns.get_loc('start')] + tasks_processing.iloc[task, tasks_processing.columns.get_loc("Time")]
                    self.set_event(start, end, summary, "Blank")
                    periods_df.iloc[time_slice, periods_df.columns.get_loc('start')] = start + tasks_processing.iloc[task, tasks_processing.columns.get_loc("Time")] + pomodoro_time
                    periods_df["Total time"] = periods_df['end'] - periods_df['start']
                    break

                elif(tasks_processing.iloc[task, tasks_processing.columns.get_loc("Time")] > periods_df.iloc[time_slice, periods_df.columns.get_loc('Total time')]):
                    # pomodoro_time_split = (periods_df.iloc[time_slice, periods_df.columns.get_loc('Total time')]/25-1)*pomodoro_break
                    pomodoro_time_split = pd.Timedelta(minutes=0)
                    tasks_processing.iloc[task, tasks_processing.columns.get_loc("Time")] = tasks_processing.iloc[task, tasks_processing.columns.get_loc("Time")] + pomodoro_time_split - periods_df.iloc[time_slice, periods_df.columns.get_loc('Total time')]
                    summary = tasks_processing.iloc[task, tasks_processing.columns.get_loc('Task')]
                    start = periods_df.iloc[time_slice, periods_df.columns.get_loc('start')]
                    end = periods_df.iloc[time_slice, periods_df.columns.get_loc('end')]
                    self.set_event(start, end, summary, "Blank")
                    periods_df.iloc[time_slice, periods_df.columns.get_loc('start')] = periods_df.iloc[time_slice, periods_df.columns.get_loc('end')]
                    periods_df["Total time"] = periods_df['end'] - periods_df['start']

                    if(tasks_processing.iloc[task, tasks_processing.columns.get_loc("Time")] <= pd.Timedelta(minutes=0)):
                        break
        
        # periods_df["Total time"] = periods_df['end'] - periods_df['start']
        list_to_remove = periods_df['id'].to_list()
        self.delete_events(list_to_remove)
        

if __name__ == '__main__':
    # main()
    pass