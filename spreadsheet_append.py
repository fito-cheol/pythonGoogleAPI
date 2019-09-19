"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Google Sheets API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/sheets
2. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""
from pprint import pprint

from googleapiclient import discovery

import pickle
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# TODO: Change placeholder below to generate authentication credentials. See
# https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample
# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
#
# Authorize using one of the following scopes:
#     'https://www.googleapis.com/auth/drive'
#     'https://www.googleapis.com/auth/drive.file'
#     'https://www.googleapis.com/auth/spreadsheets'

def spreadsheet_append_line(lines, spreadsheet_id='1AxPE64_sKhtjaAgpiZFRJPzk8YR95BuNynBzhBapFq8'):

    SCOPES = 'https://www.googleapis.com/auth/drive.file'

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = discovery.build('sheets', 'v4', credentials=creds)

    # The A1 notation of a range to search for a logical table of data.
    # Values will be appended after the last row of the table.
    range_ = 'apiSheet!A:Z'  # TODO: Update placeholder value.

    # How the input data should be interpreted.
    # https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
    value_input_option = 'RAW'  # TODO: Update placeholder value. USER_ENTERED or RAW or INPUT_VALUE_OPTION_UNSPECIFIED

    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'  # TODO: Update placeholder value. INSERT_ROWS or OVERWRITE

    value_range_body = {
        # TODO: Add desired entries to the request body.
        "majorDimension": "ROWS",
        "values": lines,
    }

    request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_,  valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)

if __name__ == '__main__':
    lines = [
            ['new', 'value', 'appended', 'here'],
            ['2 new', 'value', 'appended', 'here'],
            ['', '2 new', 'value', 'appended', 'here'],
        ]
    spreadsheet_id = '1AxPE64_sKhtjaAgpiZFRJPzk8YR95BuNynBzhBapFq8'
    spreadsheet_append_line(lines, spreadsheet_id)
