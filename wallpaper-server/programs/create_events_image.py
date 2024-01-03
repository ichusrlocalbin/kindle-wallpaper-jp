#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os
import json
import codecs
import datetime
import locale
import sys

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file

from oauth2client.service_account import ServiceAccountCredentials

import secrets

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# set id such as 'primary'
CALENDAR_ID = secrets.CALENDAR_ID

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-kindle-paperwall-jp.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def next_events():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # # show my carender_id list
    # calendar_list = service.calendarList().list().execute()
    # print(calendar_list)

    # print('Getting the upcoming 5 events')
    eventsResult = service.events().list(
        calendarId=CALENDAR_ID, timeMin=now, maxResults=5, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return format_events(events)

def format_events(events):
#    reload(sys)
#    sys.setdefaultencoding("utf-8") 
    locale.setlocale(locale.LC_ALL, ("ja_JP", "utf-8"))
    format_events = []
    for event in events:
        start_time = event['start'].get('dateTime')
        if start_time: 
            format_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S+09:00').strftime("%_H:%M")
            format_date = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S+09:00').strftime("%_m/%_d(%a)")
        else:
            format_time = ''
            format_date = datetime.datetime.strptime(event['start'].get('date'), '%Y-%m-%d').strftime("%_m/%_d(%a)")
        format_events.append((format_date, format_time, event['summary']))
    return format_events

def replace_events(format_events):
    output = codecs.open('after-weather.svg', 'r', encoding='utf-8').read()
    count = 0
    for start_date, start_time, event_name in format_events:
        output = output.replace('Day' + str(count), start_date)
        output = output.replace('Hour' + str(count), start_time)
        output = output.replace('Name' + str(count), event_name)
        count += 1
    for i in range(count, 5):
        output = output.replace('Day' + str(i), '')
        output = output.replace('Hour' + str(i) ,'')
        output = output.replace('Name' + str(i) ,'')
    codecs.open('almost_done.svg', 'w', encoding='utf-8').write(output)

def main():
    replace_events(next_events())

if __name__ == '__main__':
    main()
