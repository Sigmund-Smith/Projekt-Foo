from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread

# sagt der google api wo sie suchen soll
scope = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

#dies hier bestätigt google, dass das program auch wirklich auf die tabelle zugreifen darf
GOOGLE_SHEETS_KEY_FILE = 'the-fooprojekt-1c98624c8370.json' # pls ask admin for file
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_KEY_FILE, scope)
gc = gspread.authorize(credentials)

# wählt die richtige Tabelle aus
sheet = gc.open("Umfragedaten").sheet1
dataframe_data = pd.DataFrame(sheet.get_all_records())
#dataframe = pd.DataFrame(dataframe)
print(dataframe_data) # high iq debugging
