from typing import Dict, Any
from retriever import retriever


PROMPT = """
Find recent tweets about {topic} from {location} written in {language}.
"""

class FakeAI:
    def __init__(self):
        print("Initializing FakeAI...")

    # TODO: Uuse the retriever to get the top 1 tweet and it belongs to which author (use the retriever.py file)
    # Use this function in the generate_response function after injecting the keys from the context into the PROMPT
    # the query parameter is the string after injecting the keys from the context into the PROMPT
    async def __retrieve(self, query: str) -> Dict[str, Any]:
        # Write code here
        retrieved_docs = retriever.similarity_search(query, k=1)
        if retrieved_docs:
            doc = retrieved_docs[0]
            return {"tweet": doc.page_content, "author": doc.metadata}
        else:
            # we may raise an exception here if no documents found. like:
            # raise Exception(f"No documents found in vector store for query: {query}")
            # and handle it in the generate_response function
            # but for now, we'll just return a fake tweet and author as a fallback
            pass
        return {"tweet": "fake tweet", "author": {"name": "John Doe", "email": "john@example.com"}}

    # TODO: Inject the keys from the context into the PROMPT
    async def generate_response(self, context: Dict[str, Any]) -> Dict[str, Any]: 
        # Write code here
        # I provided default values for topic, location, and language if they are not in the context
        injected_prompt = PROMPT.format(
            topic=context.get("topic", "general"),
            location=context.get("location", "world"),
            language=context.get("language", "English")
        )


        return await self.__retrieve(injected_prompt)
    
    

