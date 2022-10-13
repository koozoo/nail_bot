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

    def update_range_values(self, range_, values, dim='ROWS'):
        data = [{
            'range': range_,
            'values': values,
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

    def create_std_list(self, val: list):
        temp = []
        for i in val:
            if len(i) < 3:
                temp.append(i + ['', '', ''])
            elif len(i) < 4:
                temp.append(i + ['', ''])
            elif len(i) < 5:
                temp.append(i + [''])
            else:
                temp.append(i)

        res = []
        l1 = []
        l2 = []
        l3 = []
        for i in temp:
            df = i[2:]
            l1.append(df[0])
            l2.append(df[1])
            l3.append(df[2])
        res.append(l1)
        res.append(l2)
        res.append(l3)

        return res

    def update_date_in_sheets(self):
        date_in_table = self.get_data_sheets('C2:C2', 'ROWS')
        dt = datetime.datetime.now()

        if date_in_table['values'][0][0][:2] != dt.strftime("%d.%m.%Y")[:2]:
            data = self.get_data_sheets('C3:AK7', 'COLUMNS')

            # delete data in calendar, and add data in db
            deleted_day = data['values'].pop(0)
            print(deleted_day)

            std_values = self.create_std_list(data['values'])
            date = [[dt.strftime("%d.%m.%Y")]]
            date_cell = 'Ежедневник!C2:C2'
            self.update_range_values(date_cell, date)

            update_date = self.get_data_sheets('C3:AK7', 'COLUMNS')

            last_day_range = 'Ежедневник!AK3:AK7'
            ld_values = [[update_date['values'][-1][0]], [update_date['values'][-1][1]], [''], [''], ['']]

            self.update_range_values(last_day_range, ld_values)
            self.update_range_values('Ежедневник!C5:AK7', std_values)

    def get_week_date(self):
        clear_data = [i for i in self.get_data_sheets('Ежедневник!C2:AK2', 'ROWS')['values'][0] if i != '']
        return [f'{"".join(clear_data[i])} - {"".join(clear_data[i+1])}' for i in range(0, len(clear_data), 2)]

def msheets():
    gs = GoogleSheet()

    range_ = 'тест!A1:C2'
    values = [
        [1, 2, 3],
        [4,  6],
        # [7, 8, 9],
    ]
    # gs.update_range_values(range_, values)
    print(gs.get_week_date())
    # gs.update_date_in_sheets()


