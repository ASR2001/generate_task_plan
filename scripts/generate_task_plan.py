import os
from typing import List, Dict, Any
from datetime import datetime

import requests
from dotenv import load_dotenv

from scripts.constants import SYSTEM_PROMPT
from scripts.search_code_base import search_code_base

load_dotenv()

AZURE_OPEN_AI_CHAT_URL = os.getenv("AZURE_OPEN_AI_CHAT_URL")
AZURE_OPEN_AI_CHAT_API_KEY = os.getenv("AZURE_OPEN_AI_CHAT_API_KEY")
QUERIES_DIR = os.path.join(os.path.dirname(__file__), "queries")


def format_code_context(search_results: List[Dict[str, Any]]) -> str:
    """Format the code search results into a string for the prompt"""
    formatted_results = []
    for result in search_results:
        formatted_results.append(
            f"File: {result['file_path']}\n```python\n{result['content']}\n```\n")
    return "\n".join(formatted_results)


def get_chat_completion(system_prompt: str, user_query: str) -> str:
    """Get chat completion from Azure OpenAI"""
    url = AZURE_OPEN_AI_CHAT_URL
    
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPEN_AI_CHAT_API_KEY
    }
    
    data = {
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        "temperature": 0,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0.5,
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error getting chat completion: {str(e)}")
        raise


def save_query_and_response(query: str, task_plan: str, code_context: str) -> None:
    """Save the query and response to a markdown file in the queries directory"""
    os.makedirs(QUERIES_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(QUERIES_DIR, f"query_{timestamp}.md")
    
    content = f"""# Task Query - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## User Query
{query}

## Task Plan
{task_plan}

## Relevant Code Context
{code_context}
"""
    
    # Save to file
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"\nQuery and response saved to: {filename}")


def generate_task_plan():
    """Main function to handle task planning"""
    user_query = input("Enter your task description: ")
    
    try:
        print("\nSearching for relevant code files...")
        search_results = search_code_base(user_query)

        code_context = format_code_context(search_results)
        system_prompt = SYSTEM_PROMPT.format(code=code_context)
        
        print("\nGenerating task plan...")
        task_plan = get_chat_completion(system_prompt, user_query)
        
        save_query_and_response(user_query, task_plan, code_context)
        
        print("\nTask Plan:")
        print("=" * 80)
        print(task_plan)
        print("=" * 80)
        
    except Exception as e:
        print(f"Error during task planning: {str(e)}")
