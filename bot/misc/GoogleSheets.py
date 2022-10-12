from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
from bot.misc.config import spreadsheet_id


class GoogleSheet:
    SPREADSHEET_ID = spreadsheet_id
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        if os.path.exists('bot/misc/token.pickle'):
            with open('bot/misc/token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'bot/misc/credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('bot/misc/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def update_range_values(self, range_, values):
        data = [{
            'range': range_,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID,
                                                                  body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

    def get_data_sheets(self, range_, dim):
        return self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID, range=range_, majorDimension=dim).execute()

    def update_date_in_sheets(self):
        date_in_table = self.get_data_sheets('C2:C2', 'ROWS')
        dt = datetime.datetime.now()
        data = self.get_data_sheets('C3:I7', 'COLUMNS')
        if date_in_table['values'][0][0][:2] != dt.strftime("%d.%m.%Y")[:2]:
            date = [[dt.strftime("%d.%m.%Y")]]
            date_cell = 'Ежедневник!C2:C2'
            self.update_range_values(date_cell, date)
            print(data)

