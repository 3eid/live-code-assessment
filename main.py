from fastapi import FastAPI, Depends, HTTPException, Request, Header
from models import create_tables, get_db, Tweet
from contextlib import asynccontextmanager

from fastapi.security import APIKeyHeader
from schemas import GenerateRequest,GenerateResponse
from config import settings
from ai import FakeAI
from sqlalchemy.orm import Session
from typing import Optional



# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


# Authentication dependency
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != settings.X_API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API Key"
        )
    return x_api_key

app = FastAPI(lifespan=lifespan)

fake_ai = FakeAI()


@app.get("/")
def read_root():
    return {"message": "Welcome to INTO AI Assessment"}


# TODO: Create an endpoint to generate ai response then save it to the database (use the ai.py and models.py file)

@app.post("/generate", response_model=GenerateResponse)
async def generate(
    request: GenerateRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
    ):
    try:
        context = {
                "topic": request.topic,
                "location": request.location,
                "language": request.language
            }
        
        response = await fake_ai.generate_response(context)

        new_tweet = Tweet(
            context=context,
            tweet=response["tweet"],
            author_name=response["author"]["name"],
            author_email=response["author"]["email"]
        )

        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
        return new_tweet
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# TODO: Retrieve all tweets from the database, sorted by author name (ascending) and created_at (descending).

