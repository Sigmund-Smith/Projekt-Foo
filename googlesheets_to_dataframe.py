from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread


scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

GOOGLE_SHEETS_KEY_FILE = 'the-fooprojekt-1c98624c8370.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_KEY_FILE, scope)
gc = gspread.authorize(credentials)


sheet = gc.open("Vorläufiges Endergebnis (Antworten)").sheet1
dataframe = sheet.get_all_records()
dataframe = pd.DataFrame(dataframe)
print(dataframe)
