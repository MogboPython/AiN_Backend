from oauth2client.service_account import ServiceAccountCredentials
import gspread
from dotenv import load_dotenv
from fastapi.exceptions import HTTPException
import os
load_dotenv()

GOOGLE_OAUTH_SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
  ]
GOOGLE_CREDENTIALS = os.getenv('CREDENTIALS')

gc = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS, GOOGLE_OAUTH_SCOPES))

"""Checks if an email address is already registered"""
def check_email(sheet: gspread.worksheet.Worksheet, column: int, email: str):
  all_values = sheet.get_all_values()
  emails = {row[column] for row in all_values}  

  if email in emails:
      raise HTTPException(status_code=400, detail="already registered")
  else:
     return None