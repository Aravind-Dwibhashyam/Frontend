from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from typing import Optional
from datetime import date

class TreatmentPlanBase(BaseModel):
    plan_id: str
    diagnosis_id: str
    goal: str
    start_date: date
    doctor_id: str

class TreatmentPlanCreate(TreatmentPlanBase):
    pass

class TreatmentPlan(TreatmentPlanBase):
    id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
