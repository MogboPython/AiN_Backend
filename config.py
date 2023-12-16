from dotenv import load_dotenv
import os
from fastapi_mail import ConnectionConfig
from pathlib import Path
load_dotenv()

class Configuration:
  CORS_EXPOSE_HEADERS = ['Content-Disposition']
  MAIL_SERVER = 'smtp.googlemail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = False
  MAIL_USE_SSL = True
  MAIL_USERNAME = os.getenv('MAIL_USERNAME')
  MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
  GOOGLE_OAUTH_SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive',
  ]
  GOOGLE_CREDENTIALS = os.getenv('CREDENTIALS')

# env = Environment(
#     loader=FileSystemLoader(searchpath="./templates"),
#     autoescape=select_autoescape(['html', 'xml'])
# )

conf = ConnectionConfig(
    MAIL_USERNAME=Configuration.MAIL_USERNAME,
    MAIL_PASSWORD=Configuration.MAIL_PASSWORD,
    MAIL_FROM=Configuration.MAIL_USERNAME,
    MAIL_PORT=Configuration.MAIL_PORT,
    MAIL_SERVER=Configuration.MAIL_SERVER,
    MAIL_FROM_NAME="AIESEC in Nigeria",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS=True,
    # TEMPLATE_FOLDER='./templates',
    TEMPLATE_FOLDER = Path(__file__).parent / 'templates',
)