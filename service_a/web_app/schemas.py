from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    name: str
