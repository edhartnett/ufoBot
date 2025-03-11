from langchain_core.tools import Tool
from typing import List, Dict
from VectorStore import UfoSiteVectorStore

vector_store = UfoSiteVectorStore()

@tool
def query_ufo_faqs(query: str) -> List[Dict[str, str]]:
    '''
    Use this tool to get information about UFOs.

    Args:
        query: The query to search for.

    Returns:
        A list of dictionaries containing the question and answer.
    '''
    return vector_store.query_faqs(query)

@tool
def query_aliens(query: str) -> List[Dict[str, str]]:
    '''
    Use this tool to get information about aliens.

    Args:
        query: The query to search for.

    Returns:
        A list of dictionaries containing the name, home system, description, and details about an alien species.
    '''
    return vector_store.query_aliens(query)
