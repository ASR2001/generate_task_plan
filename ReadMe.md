# Using generate_task_plan: A Detailed Guide

This guide provides step-by-step instructions on how to use the `generate_task_plan` functionality via the Django shell. It also explains how I created vector embeddings for the code files, store them in the Weaviate vector database, and use these embeddings to fetch relevant files when a user submits a task query.

---

## Overview

This project is set up with a clean architecture where:
- **Vector Embeddings Creation**: Each Python code file in the codebase is processed to create vector embeddings using the Azure OpenAI REST API.
- **Storage in Weaviate**: These vector embeddings (along with file metadata and content) are stored in a Weaviate collection named `CodeFile`.
- **Task Querying**: When a user submits a task description, the system retrieves the relevant code context by querying Weaviate with a vector search. Then, using the retrieved context and a system prompt (defined in our constants), it generates a detailed task plan with help of Azure OpenAI (GPT 4o).
- **Output**: The generated task plan, along with the original user query and code context, is saved as a markdown file in the `queries` folder for future reference.

---

## Prerequisites

Before you begin, ensure that:
- Your environment variables for Azure OpenAI and Weaviate are properly set (e.g., `AZURE_OPEN_AI_CHAT_URL`, `AZURE_OPEN_AI_CHAT_API_KEY`, `WEAVIATE_URL`, etc.).
- I have already indexed the codebase to populate the Weaviate collection with embeddings using the indexing script:
    ```
    python scripts/index_code_base.py
    ```
---

## Using generate_task_plan via Django Shell

Follow these steps to run the task planning from the Django shell:

1. **Open the Django Shell**  
   In your project root, open a terminal and run:
   ```
   python manage.py shell
   ```

2. **Import and Execute generate_task_plan**  
   Once in the shell, import the function and run it:
   ```python
   from scripts.generate_task_plan import generate_task_plan
   generate_task_plan()
   ```
   
3. **Input Your Task Description**  
   The function will prompt you:
   ```
   Enter your task description:
   ```
   Type your task description, for example,  
   `I want to support the creation of user access with multiple interviews`
   and press Enter.

4. **Processing and Output**  
   - The script calls a search function that uses the Azure OpenAI text embedding API to generate a vector embedding for your query.
   - It then creates a Weaviate client, searches the `CodeFile` collection, and retrieves the most relevant code snippets from the codebase.
   - The relevant code context is formatted and injected into a system prompt (as defined in `scripts/constants.py`), and then sent to Azure OpenAI for generating the task plan.
   - Finally, the generated task plan is printed on the console and saved as a markdown file in the `queries` folder.

---

## How Vector Embeddings Are Created and Stored

1. **Embedding Generation**  
   - In `scripts/index_code_base.py`, the function `get_azure_embedding` sends the content of each Python code file to the Azure OpenAI embedding API.
   - It receives a vector (list of floats) representing the semantic content of the file.

2. **Storage in Weaviate**  
   - The script uses a Weaviate client (created using `create_weaviate_client`) to connect to the Weaviate cloud instance.
   - It then indexes each file by adding it to a collection named `CodeFile`, along with its file path and content.
   - This setup makes it possible to perform efficient similarity searches based on vector representations when queries are received.

---

## How Task Queries Are Processed

1. **User Query Submission**  
   - When you run `generate_task_plan()`, you provide a task description.
   
2. **Fetching Relevant Code Context**  
   - The function `search_code_base` uses the provided query to generate a query vector.
   - This vector is then used to perform a nearest-neighbor search in the `CodeFile` collection on Weaviate.
   - Relevant code snippets (based on similarity) are fetched and formatted using `format_code_context`.

3. **Generating the Task Plan**  
   - The formatted code context is embedded into a system prompt (defined in `scripts/constants.py`).
   - This complete prompt, along with your task description, is sent to Azure OpenAI using the `get_chat_completion` function.
   - The API returns a structured task plan which explains the required implementation steps.
   
4. **Saving Results**  
   - The final task plan, along with the original query and the relevant code context, is saved as a markdown file in the `queries` directory.
   - Each file is timestamped so you can easily track and review past task plans.

---

## Viewing the Generated Task Plan

- After running the script, you will see a confirmation message on the console indicating the file path where the query and the task plan were saved.
- Navigate to the `queries` folder in your project root to open and review the generated markdown file. It contains:
  - The original user query.
  - The structured task plan generated by the system.
  - The code context (including file names and code snippets) that was used to generate the plan.

---

## Example Walkthrough

1. **Run the shell and import the module:**
   ```python
   >>> from scripts.generate_task_plan import generate_task_plan
   >>> generate_task_plan()
   ```
2. **At the prompt, enter:**
   ```
   I want to support the creation of user access with multiple interviews
   ```
3. **Behind the scenes:**
   - The system searches through your codebase by computing vector embeddings.
   - It fetches files that are closest in meaning to your provided task query.
   - A detailed implementation plan is generated based on the code context and your task description.
4. **Result:**  
   The task plan is printed in the console and saved in a file (e.g., `queries/query_20250204_160910.md`) inside the `queries` folder.

---

## Conclusion

By following the steps in this guide, you can easily generate a detailed task plan for your Django project using the `generate_task_plan` functionality. The process leverages state-of-the-art vector embeddings and a cloud-based vector database (Weaviate) to retrieve the necessary code context, ensuring that the task plans are both relevant and actionable. The entire output, including the original query and embedded code context, is stored for future reference in the `queries` folder.

Happy coding!
