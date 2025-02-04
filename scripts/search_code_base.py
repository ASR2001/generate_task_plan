import os
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth, AdditionalConfig, Timeout

load_dotenv()

AZURE_OPENAI_TEXT_EMBEDDING_URL = os.getenv("AZURE_OPENAI_TEXT_EMBEDDING_URL")
AZURE_OPENAI_TEXT_EMBEDDING_API_KEY = os.getenv(
    "AZURE_OPENAI_TEXT_EMBEDDING_API_KEY")

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")


def get_vector_embedding(text: str) -> List[float]:
    """Get embeddings using Azure OpenAI REST API"""
    url = AZURE_OPENAI_TEXT_EMBEDDING_URL
    
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_TEXT_EMBEDDING_API_KEY
    }
    
    data = {
        "input": text,
        "encoding_format": "float"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
    except Exception as e:
        print(f"Error getting embeddings: {str(e)}")
        raise


def create_weaviate_client():
    """Create and return a Weaviate client"""
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
        additional_config=AdditionalConfig(timeout_=Timeout(init=60)),
    )
    return client


def search_code_base(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    query_embedding = get_vector_embedding(query)
    
    client = create_weaviate_client()
    
    try:
        collection = client.collections.get("CodeFile")
        
        results = (
            collection.query
            .near_vector(
                near_vector=query_embedding,
                limit=limit
            )
        )
        
        matches = []
        for obj in results.objects:
            matches.append({
                "file_path": obj.properties["file_path"],
                "content": obj.properties["content"],
            })
        
        return matches
        
    finally:
        client.close()


def main():
    """Main function to handle user input and display results"""
    query = input("Enter your search query: ")
    
    try:
        results = search_code_base(query)
        
        print("\nSearch Query:", query)
        print("\nMatching Files:")
        print("-" * 80)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. File: {result['file_path']}")
            print("Content:")
            print("-" * 40)
            print(result['content'])
            print("-" * 80)
            
    except Exception as e:
        print(f"Error during search: {str(e)}")
