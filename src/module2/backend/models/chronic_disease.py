from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated
from typing import Optional

class ChronicDiseaseBase(BaseModel):
    disease_id: str
    name: str
    type: str
    description: Optional[str] = None

class ChronicDiseaseCreate(ChronicDiseaseBase):
    pass

class ChronicDisease(ChronicDiseaseBase):
    id: Annotated[str, BeforeValidator(str)] | None = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
