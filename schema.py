from pydantic import BaseModel, EmailStr 
from typing import Union, List, Any, Dict
# from pydantic_settings import BaseSettings

class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any]

class UserEmail(BaseModel):
    email: EmailStr

class Delegate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    state_residence: str
    occupation: Union[str, None] = None
    school: Union[str, None] = None
    expectations: str
    sdg_knowledge: str
    join_event: str
    hear_about_event: str

class Guest(BaseModel):
    name: str
    email: EmailStr
    ticket_type: str
    other_names: Union[str, None] = None
    suggestions: Union[str, None] = None

class Recruit(BaseModel):
    first_name: str
    last_name: str
    dob: Union[str, None] = None
    email: EmailStr
    phone: str
    academic_situation: str
    residence: Union[str, None] = None
    school_location: Union[str, None] = None
    name_of_school: Union[str, None] = None
    other_names: Union[str, None] = None
    course: Union[str, None] = None
    level: Union[str, None] = None
    aiesec_participation: Union[bool, None] = None
    event_participated: Union[str, None] = None
    motivation: Union[str, None] = None
    interest: str
    skills: Union[str, None] = None
    hear_about_recruitment: Union[str, None] = None

class NCJOS(BaseModel):
    name: str
    ravenCoordinates: str
    gender: str
    email: EmailStr
    lc: str
    birthday: str
    rank: str
    emergencyContact: str
    allergies: Union[str, None] = None
    allergyTreatment: Union[str, None] = None
    oppositeSexCompatibility: bool
    firstSummit: bool
    emergencyContactRelationship: str
    suggestions: Union[str, None] = None


# class Config(BaseSettings):
#     GOOGLE_CREDENTIALS: any
#     GOOGLE_OAUTH_SCOPES: any

#     class Config:
#         env_file = ".env"

# config = Config()