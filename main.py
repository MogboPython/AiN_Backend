from schema import *
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from utils.helper_functions import split_name, split_university
from utils.mail import send_email_async
from utils.sheet import gc, check_email


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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    detail = exc.errors()[0]["msg"]
    return JSONResponse(status_code=422, content={"detail": detail})

def submit_to_sheet(email: str):
    sheet = gc.open('Website Email Signups').sheet1
    emails = {item for item in sheet.col_values(1) if item}

    if email in emails:
        raise HTTPException(status_code=400, detail="already registered")
    else:
        sheet.append_row([email])
    
def submit_recruit(recruit: Recruit):
    name_of_school = recruit.name_of_school 
    school_location = recruit.school_location
    
    if recruit.other_names != "":
        university, state = split_university(recruit.other_names)
        name_of_school = university
        school_location = state

    sheet = gc.open('AiN 2024 Recruitment Sheet').sheet1 
    check_registered_email = check_email(sheet, 3, recruit.email)

    if check_registered_email == None:
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
    check_registered_email = check_email(sheet, 3, ncjos.email)

    if check_registered_email == None:
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

@app.get("/api/healthcheck")
def read_root():
    return {"status": "ok"}

@app.post("/api/submit_email")
async def submit_email(email: UserEmail):
    submit_to_sheet(email.email)
    return {"detail":"registration success"}

# Api endpoint for NC Jos
@app.post("/api/register_for_ncjos")
async def register(ncjos: NCJOS):
    first_name, last_name, email, lc = submit_nc_jos_data(ncjos)
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

if __name__ == "__main__":
    app.run()