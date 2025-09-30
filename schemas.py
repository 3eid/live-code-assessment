
# TODO: Create the pydantic schemas for the endpoints (use models.py as reference)

from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Dict


class GenerateRequest(BaseModel):
    topic:str
    location:str
    language:str


class GenerateResponse(BaseModel):
    id: int = Field(..., description="Unique ID of the tweet")
    context: Dict = Field(..., description="Context information as JSON")
    tweet: str = Field(..., description="The tweet text")
    author_name: str = Field(..., description="Name of the author")
    author_email: EmailStr = Field(..., description="Email of the author")
    created_at: datetime = Field(..., description="Creation timestamp")

    # because we will return the SQLAlchemy model instance in the endpoint
    class Config:
        from_attributes = True  

class GetTweetsResponse(BaseModel):
    tweets: list[GenerateResponse]