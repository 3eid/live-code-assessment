from fastapi import FastAPI, Depends, HTTPException, Header
from models import create_tables, get_db, Tweet
from contextlib import asynccontextmanager

from schemas import GenerateRequest,GenerateResponse,GetTweetsResponse
from config import settings
from ai import FakeAI
from sqlalchemy.orm import Session
from typing import Optional, List
from background import cleanup_author_old_tweets
from fastapi import BackgroundTasks


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
    background_tasks: BackgroundTasks,
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

        # Add background task to cleanup old tweets for the same author
        background_tasks.add_task(cleanup_author_old_tweets, new_tweet.author_email, db)
        
        return new_tweet
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# TODO: Retrieve all tweets from the database, sorted by author name (ascending) and created_at (descending).


@app.get("/tweets", response_model=GetTweetsResponse)
async def get_tweets(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
    ):
    """Retrieve all tweets sorted by author name (asc) and created_at (desc)"""
    tweets = db.query(Tweet).order_by(
        Tweet.author_name.asc(),
        Tweet.created_at.desc()
    ).all()
    
    return {"tweets":tweets}