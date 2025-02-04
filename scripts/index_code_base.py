import os
from typing import List, Optional

import requests
from pathlib import Path
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth, AdditionalConfig, Timeout
from weaviate.classes.config import Property, DataType, Configure

load_dotenv()

AZURE_OPENAI_TEXT_EMBEDDING_URL = os.getenv("AZURE_OPENAI_TEXT_EMBEDDING_URL")
AZURE_OPENAI_TEXT_EMBEDDING_API_KEY = os.getenv(
    "AZURE_OPENAI_TEXT_EMBEDDING_API_KEY")

WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

DJANGO_ROOT = os.getenv("DJANGO_ROOT")


def get_azure_embedding(text: str) -> Optional[List[float]]:
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
        return None


def init_weaviate_collection(client: weaviate.WeaviateClient):
    """Initialize Weaviate collection"""
    collection_name = "CodeFile"
    if collection_name not in client.collections.list_all():
        client.collections.create(
            name=collection_name,
            properties=[
                Property(name="file_path", data_type=DataType.TEXT),
                Property(name="content", data_type=DataType.TEXT),
            ],
            vectorizer_config=Configure.Vectorizer.none()
        )
        print(f"Collection '{collection_name}' created successfully")
    else:
        print(f"Collection '{collection_name}' already exists")


def index_code_base(client: weaviate.WeaviateClient, root_dir: str):
    """Process directory and store embeddings"""
    root_path = Path(root_dir)
    collection = client.collections.get("CodeFile")

    excluded_dirs = {'scripts', 'venv', '.specstory'}

    for file_path in root_path.glob('**/*'):
        should_process_the_file = (
            file_path.is_file() and '.py' in file_path.suffix and
            not any(excluded_dir in file_path.parts for excluded_dir in
                    excluded_dirs)
        )

        if not should_process_the_file:
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

                if not content.strip():
                    continue

                embedding = get_azure_embedding(content)
                if not embedding:
                    raise Exception("Failed to get embedding")

                collection.data.insert(
                    properties={
                        "file_path": str(file_path.relative_to(root_path)),
                        "content": content
                    },
                    vector=embedding
                )
                print(f"Processed: {file_path.relative_to(root_path)}")

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")


def create_weaviate_client():
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
        additional_config=AdditionalConfig(timeout_=Timeout(init=60)),
    )
    return client


def main():
    client = create_weaviate_client()
    init_weaviate_collection(client)
    index_code_base(client, DJANGO_ROOT)
