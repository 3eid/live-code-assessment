# TODO: BONUS
# Use fastapi background task, after generate the ai response and saving it to the database,
# check if their is a tweet in the database with the same author email, if yes then delete the oldest tweet for that author


from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from models import Tweet


# I assumed that if there are multiple tweets from the same author (same email),
# we will delete the oldest tweet (based on created_at timestamp)

def cleanup_author_old_tweets(author_email: str, db: Session):
    """Delete the oldest tweet if multiple tweets exist for the given author email"""
    tweets = (
        db.query(Tweet)
        .filter(Tweet.author_email == author_email)
        .order_by(Tweet.created_at.asc())  # oldest first
        .all()
    )
    
    if len(tweets) > 1:
        oldest_tweet = tweets[0]  # the first one since asc order
        db.delete(oldest_tweet)
        db.commit()
