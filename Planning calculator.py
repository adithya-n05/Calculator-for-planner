from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import os
import pytz
import argparse

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_free_hours(service, start_hour, end_hour, days):
    try:
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
        end_date = (datetime.datetime.utcnow().replace(tzinfo=pytz.UTC) + datetime.timedelta(days=days)).isoformat()
        calendar_id = 'primary'
        events_result = service.events().list(calendarId=calendar_id, timeMin=now,
                                              timeMax=end_date, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        
        free_hours = {}
        total_free_hours = 0
        
        for i in range(days):
            current_day = (datetime.datetime.utcnow() + datetime.timedelta(days=i)).date()
            free_hours[current_day] = 0

            day_start = datetime.datetime.combine(current_day, datetime.time(start_hour, 0)).replace(tzinfo=pytz.UTC)
            day_end = datetime.datetime.combine(current_day, datetime.time(end_hour, 0)).replace(tzinfo=pytz.UTC)

            free_intervals = [(day_start, day_end)]

            for event in events:
                event_start = datetime.datetime.fromisoformat(event['start'].get('dateTime'))
                event_end = datetime.datetime.fromisoformat(event['end'].get('dateTime'))

                for interval_start, interval_end in free_intervals[:]:
                    if interval_start < event_start < interval_end:
                        free_intervals.remove((interval_start, interval_end))
                        if interval_start < event_start:
                            free_intervals.append((interval_start, event_start))
                        if event_end < interval_end:
                            free_intervals.append((event_end, interval_end))

            for interval_start, interval_end in free_intervals:
                free_hours[current_day] += (interval_end - interval_start).total_seconds() / 3600

            total_free_hours += free_hours[current_day]

        return free_hours, total_free_hours

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def main():
    print("Welcome to the time calculator script. Enter the starting time for each day")
    start_hour = input("Start time:")
    start_hour = int(start_hour)
    end_hour = input("End time:")
    end_hour = int(end_hour)
    days = input("Number of days:")
    days = int(days)
    

    service = authenticate_google_calendar()

    free_hours, total_free_hours = get_free_hours(service, start_hour, end_hour, days)

    if free_hours is not None:
        print("Free hours per day:")
        for day, hours in free_hours.items():
            print(f"{day}: {hours:.2f} hours")
        print(f"Total free hours over {days} days: {total_free_hours:.2f} hours")

if __name__ == '__main__':
    main()
