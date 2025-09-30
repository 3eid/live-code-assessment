# TODO: BONUS
# Use fastapi background task, after generate the ai response and saving it to the database,
# check if their is a tweet in the database with the same author email, if yes then delete the oldest tweet for that author


from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from models import Tweet, get_db


# I assumed that if there are multiple tweets from the same author (same email),
# we will delete the oldest tweet (based on created_at timestamp)

def cleanup_author_old_tweets(author_email: str):
    """Delete the oldest tweet if multiple tweets exist for the given author email"""
    db: Session = next(get_db())
    try:
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
    finally:
        db.close()

# better approach through one query to delete the oldest tweet if multiple exist
def cleanup_author_old_tweets_optimized(author_email: str):
    """Delete the oldest tweet if multiple tweets exist for the given author email
    This approach uses a subquery to find the oldest tweet and delete it in one go.
    it's better than fetching all tweets and then deleting one.
    single query + not fetching all tweets into memory (better for performance and scalability)
    """
    db: Session = next(get_db())
    try:
        subquery = (
            db.query(Tweet.id)
            .filter(Tweet.author_email == author_email)
            .order_by(Tweet.created_at.asc())
            .limit(1)   # only get one tweet to delete
            .subquery()
        )

        db.query(Tweet).filter(Tweet.id.in_(subquery)).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()