from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from typing import Optional
from datetime import date

class PatientBase(BaseModel):
    patient_id: str
    name: str
    dob: date
    age: int
    gender: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
