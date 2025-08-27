from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecievedItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    recieved_at: datetime
