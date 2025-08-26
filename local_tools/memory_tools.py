"""Tools to search through local memory store."""

import json
from typing import Any
import requests

from flock.core import flock_tool
from flock.core.logging.logging import get_logger

import settings

MEMORY_BASE_URL = settings.APP_SETTINGS.memory_upload_url.replace("/api/v1/embed", "/api/v1/")

LOGGER = get_logger("tools.kernel_memory")


@flock_tool
async def check_knowledge_base_health() -> str:
    """Check if the Memory store is healthy and available for search.
    Takes no arguments.

    Returns:
        status: str -> If healthy: "healthy", otherwise: "unhealthy"
    """

    health_endpoint = "health"

    try:
        # send the request
        result = requests.get(url=f"{MEMORY_BASE_URL.replace('/api/v1/', '/api/ui/')}{health_endpoint}")
        
        if result.status_code == 200:
            return "healthy"
        
        else:
            LOGGER.error(
                f"Tool: 'check_if_memory_available': unhealthy: {result.status_code}"
            )
            return "unhealthy"

    except Exception as e:
        LOGGER.error(f"Tool: 'check_if_memory_available': {e}")
        return "unhealthy"

def parse_query_result(result_body: dict[str, Any]) -> list[dict[str, Any]]:
    
    result_list: list[dict[str, Any]] = []
    

    
    for result in result_body:
        # format the result.
        data = result.get("data")
        score = result.get("score")
        
        # a list of dicts
        contents: list[str] = []
        for entry in data:
            page_content = entry.get("page_content")
            contents.append(page_content)
        
        result_list.append({
            'document_contents': contents,
            'score': score
        })
    
    return result_list

def parse_answer(answer_object: dict[str, Any]) -> dict[str, Any]:
    
    textual_answer = answer_object.get("text", "No answer provided")
    relevant_sources = []
    # now for the relevant sources.
    sources = answer_object.get("relevantSources", [])
    
    for source in sources:
        source_name = source.get("sourceName", "")
        index = source.get("index", "")
        parsed_partitions = []
        partitions = source.get("partitions", [])
        
        for partition in partitions:
            text = partition.get("text", "")
            relevance = partition.get("relevance", 0.0)
            
            parsed_partitions.append({
                "text": text,
                "relevance": relevance,
            })
        
        relevant_sources.append({
            "source_name": source_name,
            "index": index,
            "partitiions": partitions
        })
    
    return {
        "answer": textual_answer,
        "relevant_sources": relevant_sources,
    }

@flock_tool
async def search_knowledge_base(
    query: str,
    minimum_relevance: float,
    limit: int,
) -> list[dict[str, Any]] | str:
    """Search the knowledge base for relevant snippets of text.
    
    Args:
        query: str -> A query in natural language that is used to perform semantic search.
        minimum_relevance: float -> an number between 0.1 and 1.0. Relevance ranking is based on cosine similarity of stored embeddings. Higher values result in a more strict search.
        limit: int -> How many results to return at most. For example: if limit is set to 5, only the top 5 results will be returned.
    
    Returns:
        results: list[dict[str, Any]] -> Results of the query if the correct arguments were provided.
        OR error_message: str -> if arguments were provided incorrectly, the error_message indicates what went wrong in the tool call.
    """
    
    search_endpoint = "query_all"
    
    url = f"{MEMORY_BASE_URL}{search_endpoint}"
    
    api_key = settings.APP_SETTINGS.azure_api_key
    
    if query == "" or query is None:
        return "query cannot be empty"
    if minimum_relevance < 0.1 or minimum_relevance > 1.0:
        return "minimum_relevance must be a positive value between 0.1 and 1.0"
    if limit <= 0:
        return "limit cannot be negative and must be greater than 0"
    
    # now that verification is done, send the request
    try:
        response = requests.post(
            url=url,
            json={
                "query": query,
                "min_relevance": minimum_relevance,
                "max_results": limit,
            },
            headers={
                'api-key': api_key
            }
        )
        
        if response.status_code == 200:
            body = response.content.decode()
            body_dict: dict[str, Any] = json.loads(body)
            search_results: list[dict[str, Any]] = parse_query_result(body_dict)
            return search_results
        else:
            return f"Provided parameters were correct but knowledge-base responded with status: {response.status_code}"
    except Exception as e:
        LOGGER.error(
            f"Tool: 'search_knowledge_base': Error: {e}"
        ) 
        return f"Provided parameters were correct but knowledge-base returned an Error: {e}"