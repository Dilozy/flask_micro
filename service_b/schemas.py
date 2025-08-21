from datetime import datetime

from pydantic import BaseModel


class RecievedItemRead(BaseModel):
    id: int
    name: str
    recieved_at: datetime

    class Config:
        from_attributes = True
