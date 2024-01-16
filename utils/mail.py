from dotenv import load_dotenv
import os
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from fastapi.exceptions import RequestValidationError, HTTPException
from pathlib import Path
# from ..utils.sheet import gc

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_USERNAME'),
    MAIL_PORT = 587,
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_FROM_NAME="AIESEC in Nigeria",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER = Path(__file__).resolve().parents[1] / 'templates',
)
print(Path(__file__).resolve().parent.parent)

async def send_email_async(subject: str, email_to: str, body: dict, template: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)

    await fm.send_message(message, template_name=template)

# def check_email(email:str, column_number:int):
#     sheet = gc.open('Leadership Summit Registration Sheet').sheet1
#     all_values = sheet.get_all_values()
#     emails = [row[column_number] for row in all_values] 

#     if email in emails:
#         raise HTTPException(status_code=400, detail="already registered")
#     else: 
#         return Tru