from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    type: str
    timestamp: Optional[datetime] = datetime.utcnow()
    payload: dict


class EventUpdate(BaseModel):
    type: Optional[str] = None
    timestamp: Optional[datetime] = None
    payload: Optional[dict] = None
    # Add any other fields you want to be updatable

    class Config:
        # orm_mode = True  - it will still work in Pydantic V1
        model_config = ConfigDict(from_attributes=True)


class EventOut(BaseModel):
    id: str
    type: str
    timestamp: datetime
    payload: dict

    class Config:
       model_config = ConfigDict(from_attributes=True)
