from schema import *
from config import Configuration, conf
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, MessageType
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

config = Configuration()

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gc = gspread.authorize(ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE_CREDENTIALS, config.GOOGLE_OAUTH_SCOPES))

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    detail = exc.errors()[0]["msg"]
    return JSONResponse(status_code=422, content={"detail": detail})

async def send_email_async(subject: str, email_to: str, body: dict, template: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)

    await fm.send_message(message, template_name=template)

def split_name(name):
    name_parts = name.split(" ")
    first_part = name_parts[0]
    last_part = " ".join(name_parts[1:])
    return first_part, last_part

def split_university(name):
    university_parts = name.split(",")
    first_part = university_parts[0]
    last_part = ",".join(university_parts[1:])
    return first_part, last_part

def get_serial_number(number: int):
    if number < 10:
        return "00" + str(number)
    elif number >= 10 and number < 100:
        return "0" + str(number)
    else:
        return str(number)

def submit_to_sheet(email: str):
    sheet = gc.open('Website Email Signups').sheet1
    emails = [item for item in sheet.col_values(1) if item]

    if email in emails:
        raise HTTPException(status_code=400, detail="already registered")
    else:
        sheet.append_row([email])

# def submit_delegate(delegate: Delegate):
#     sheet = gc.open('Leadership Summit Registration Sheet').sheet1
#     all_values = sheet.get_all_values()
#     emails = [row[2] for row in all_values]  

#     if delegate.email in emails:
#         raise HTTPException(status_code=400, detail="already registered")
#     else:
#         num_of_rows = len(all_values)
#         delegate_id = "LS23" + get_serial_number(num_of_rows)
#         sheet.append_row([
#             delegate_id,
#             delegate.name, 
#             delegate.email, 
#             delegate.phone, 
#             delegate.state_residence, 
#             delegate.occupation, 
#             delegate.school, 
#             delegate.expectations, 
#             delegate.sdg_knowledge,
#             delegate.join_event,
#             delegate.hear_about_event
#         ])

#         first_name, _ = split_name(delegate.name)
#         return delegate_id, first_name
    
def submit_recruit(recruit: Recruit):
    name_of_school = recruit.name_of_school 
    school_location = recruit.school_location
    
    if recruit.other_names != "":
        university, state = split_university(recruit.other_names)
        name_of_school = university
        school_location = state

    sheet = gc.open('AiN 2024 Recruitment Sheet').sheet1
    all_values = sheet.get_all_values()
    emails = [row[3] for row in all_values]  

    if recruit.email in emails:
        raise HTTPException(status_code=400, detail="already registered")
    else:
        sheet.append_row([
            recruit.first_name,
            recruit.last_name,
            recruit.dob, 
            recruit.email,
            recruit.phone,
            recruit.academic_situation,
            recruit.residence,
            school_location,
            name_of_school,
            recruit.course,
            recruit.level,
            recruit.aiesec_participation,
            recruit.event_participated,
            recruit.motivation,
            recruit.interest,
            recruit.skills,
            recruit.hear_about_recruitment
        ])

        return recruit.first_name, recruit.email

# Callback function for the ncjos endpiont
def submit_nc_jos_data(ncjos: NCJOS):
    sheet = gc.open('NC Jos Conference Signups').sheet1
    all_values = sheet.get_all_values()
    emails = [row[3] for row in all_values]  

    if ncjos.email in emails:
        raise HTTPException(status_code=400, detail="This user already exists")
    else:
        created_at = datetime.now().strftime("%d/%m/%Y %H:%M")
        sheet.append_row([
            ncjos.name,
            ncjos.ravenCoordinates,
            ncjos.gender,
            ncjos.email, 
            created_at,
            ncjos.lc,
            ncjos.birthday,
            ncjos.rank,
            ncjos.firstSummit,
            ncjos.allergies,
            ncjos.allergyTreatment,
            ncjos.oppositeSexCompatibility,
            ncjos.emergencyContact,
            ncjos.emergencyContactRelationship,
            ncjos.suggestions
        ])
        first_name, last_name = split_name(ncjos.name)

        return first_name, last_name, ncjos.email, ncjos.lc
    
def submit_guest(guest: Guest):
    sheet = gc.open('Eclipse Dinner Guests').sheet1
    all_values = sheet.get_all_values()
    emails = [row[1] for row in all_values]  

    if guest.email in emails:
        raise HTTPException(status_code=400, detail="already registered")
    else:
        sheet.append_row([
            guest.name,
            guest.email,
            guest.ticket_type,
            guest.other_names,
            guest.suggestions
        ])

        return guest.name


@app.get("/api/healthcheck")
def read_root():
    return {"status": "ok"}

@app.post("/api/submit_email")
async def submit_email(email: UserEmail):
    submit_to_sheet(email.email)
    return {"detail":"registration success"}

# @app.post("/api/register_delegate")
# async def register(delegate: Delegate):
#     delegate_id, first_name = submit_delegate(delegate)
#     await send_email_async(
#         'Leadership Summit Confirmation', 
#         delegate.email, 
#         {
#             "first_name" : first_name,
#             "delegate_id" : delegate_id
#         },
#         'email_template.html'
#     )
#     return {"detail":"registration success", }

# Api endpoint for NC Jos
@app.post("/api/register_for_ncjos")
async def register(ncjos: NCJOS):
    first_name, last_name, email, lc = submit_nc_jos_data(ncjos)
    # ticket = "https://henceee.fly.dev/nts-enugu/generate-ticket?firstName=" + first_name + "&lastName=" + last_name + "&localCom=" + payload["localCom"]
    # ticket = f"127.0.0.1:5000/nc-jos/generate-ticket?firstName={first_name}&lastName={last_name}&localCom={lc}"
    ticket = f"https://henceee.fly.dev/nc-jos/generate-ticket?firstName={first_name}&lastName={last_name}&localCom={lc}"
    await send_email_async(
        'Welcome Aboard!', 
        email, 
        {
            "first_name" : first_name,
            "ticket": ticket,
        },
        'email.html'
    )
    created = {
        'status' : True,
        'message' : 'Registeration Successfull'
    }
    return created, 201

@app.post("/api/recruitment")
async def register(recruit: Recruit):
    first_name, email = submit_recruit(recruit)
    await send_email_async(
        'Confirmation Email for Recruitment', 
        email, 
        {
            "first_name": first_name
        },
        'recruitment_email_template.html'
    )
    return {"detail":"registration success"}  

@app.post("/api/dinner_registration")
async def dinner_registration(guest: Guest):
    _ = submit_guest(guest)
    return {"detail":"registration success"}

if __name__ == "__main__":
    app.run()