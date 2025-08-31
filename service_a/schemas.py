from datetime import datetime

from pydantic import BaseModel, ConfigDict, Json


class ItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: str


class ItemRead(BaseModel):
    id: int
    name: str
    created_at: datetime


class OutboxEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    payload: Json
    created_at: datetime
    processed: bool
