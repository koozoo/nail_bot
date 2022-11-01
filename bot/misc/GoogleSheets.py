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

    def get_data_sheets(self, range_, dim='ROWS'):
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

            last_day_range = 'Ежедневник!AK5:AK7'
            ld_values = [[''], [''], ['']]

            #update last date
            self.update_range_values(last_day_range, ld_values)
            #update all table
            self.update_range_values('Ежедневник!C5:AK7', std_values)

    def get_week_date(self):
        clear_data = [i for i in self.get_data_sheets('Ежедневник!C2:AK2', 'ROWS')['values'][0] if i != '']
        return [f'{"".join(clear_data[i])} - {"".join(clear_data[i+1])}' for i in range(0, len(clear_data), 2)]

    def get_available_day(self, week):
        num = [i for i in week.split(' ') if i.isdigit()]
        week_in_table = [[j for j in i.split(' ') if j.isdigit()] for i in self.get_week_date()]

        week_range = {
            0: 'Ежедневник!C3:I7',
            1: 'Ежедневник!J3:P7',
            2: 'Ежедневник!Q3:W7',
            3: 'Ежедневник!X3:AD7',
            4: 'Ежедневник!AE3:AK7'
        }
        res = []

        for i in week_in_table:

            if i == num:
                range_ = week_range[week_in_table.index(num)]
                data = self.get_data_sheets(range_, 'COLUMNS')

                lst_data = data['values']
                for i in range(len(lst_data)):
                    if len(lst_data[i][2:]) == 3 and '' not in lst_data[i][2:]:
                        continue
                    else:
                        res.append([lst_data[i], i])
        return res

    def get_time_in_day(self, d):
        range_ = 'Ежедневник!C3:AK7'
        days = self.get_data_sheets(range_, 'COLUMNS')
        temp = []
        for day in days['values']:
            if len(day) < 3:
                temp.append(day + ['', '', ''])
            elif len(day) < 4:
                temp.append(day + ['', ''])
            elif len(day) < 5:
                temp.append(day + [''])
            else:
                temp.append(day)

        for i in temp:
            if i[0] == d:
                res = [(i[j], j) for j in range(2, len(i)) if i[j] == '']
                return res

    def get_title_time(self):
        range_ = 'Ежедневник!B5:B7'
        time = self.get_data_sheets(range_)
        return time['values']

    def get_col_addres(self, day):
        days_dict = {
            0: 'C3:C7',
            1: 'D3:D7',
            2: 'E3:E7',
            3: 'F3:F7',
            4: 'G3:G7',
            5: 'H3:H7',
            6: 'I3:I7',
            7: 'J3:J7',
            8: 'K3:K7',
            9: 'L3:L7',
            10: 'M3:M7',
            11: 'N3:N7',
            12: 'O3:O7',
            13: 'P3:P7',
            14: 'Q3:Q7',
            15: 'R3:R7',
            16: 'S3:S7',
            17: 'T3:T7',
            18: 'U3:U7',
            19: 'V3:V7',
            20: 'W3:W7',
            21: 'X3:X7',
            22: 'Y3:Y7',
            23: 'Z3:Z7',
            24: 'AA3:AA7',
            25: 'AB3:AB7',
            26: 'AC3:AC7',
            27: 'AD3:AD7',
            28: 'AE3:AE7',
            29: 'AF3:AF7',
            30: 'AG3:AG7',
            31: 'AH3:AH7',
            32: 'AI3:AI7',
            33: 'AJ3:AJ7',
            34: 'AK3:AK7',
        }
        return days_dict[day]

    def get_target_cell(self, range_, time):
        dc = {
            2: 5,
            3: 6,
            4: 7,
            '10:00': 5,
            '15:00': 6,
            '18:00': 7
        }
        if len(range_) == 7:
            return f'{range_[:2]}{dc[time]}:{range_[:2]}{dc[time]}'
        else:
            return f'{range_[:1]}{dc[time]}:{range_[:1]}{dc[time]}'

    def write_order_in_table(self, calback_value, contact_value):
        print(calback_value)
        call = calback_value.split('_')

        day = call[1].replace("$", ".")

        time = call[2]
        time_unit = self.get_title_time()
        time_unit_dict = {
            2: ''.join(time_unit[0]),
            3: ''.join(time_unit[1]),
            4: ''.join(time_unit[2])
        }

        range_ = 'Ежедневник!C3:AK7'
        all_days = self.get_data_sheets(range_, 'COLUMNS')['values']

        temp = []
        for d in all_days:
            if len(d) < 3:
                temp.append(d + ['', '', ''])
            elif len(d) < 4:
                temp.append(d + ['', ''])
            elif len(d) < 5:
                temp.append(d + [''])
            else:
                temp.append(d)
        data = [['\n'.join(str(i) for i in contact_value if i != None)]]

        for i, d in enumerate(temp):
            if day in d:
                target_cell = self.get_target_cell(self.get_col_addres(i), int(time))
                self.update_range_values(target_cell, data)
                return target_cell

    def del_order(self, cell):
        if len(cell) == 5:
            range_ = f"Ежедневник!{cell[:2]}"
        else:
            range_ = f"Ежедневник!{cell[:3]}"
        body = {}
        self.service.spreadsheets().values().clear(spreadsheetId=self.SPREADSHEET_ID, range=range_,
                                                        body=body).execute()

    def update_order(self, cell, data):
        self.del_order(cell)
        self.update_range_values(cell, data)
