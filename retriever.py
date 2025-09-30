import json

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.embeddings import FakeEmbeddings



embeddings = FakeEmbeddings(size=768)



# TODO: Load data/tweets.json
# page content is the tweet text
# the metadata is the author information

tweets = []
with open("data/tweets.json", "r") as f:
    tweets_list = json.load(f)
    for tweet in tweets_list:
        # I used the dict.get method to provide default values as fallback in case the keys are missing (used fake tweet)
        tweets.append(
            Document(
                page_content=tweet.get("tweet", "fake tweet"),
                metadata=tweet.get("author", {"name": "John Doe", "email": "john@example.com"})
                )
        )

retriever = FAISS.from_documents(tweets, embeddings)
