# Question-Answer Agentic AI
This repository contains a simple agentic AI system designed for question-answering. The agent can handle queries by either retrieving facts from a local knowledge base or by leveraging a Large Language Model (LLM) for more conversational or complex questions. It is built using FastAPI and LangChain, with examples demonstrating agentic graph construction using LangGraph.

## Features

- **Hybrid Answering System**: Uses a local, fast search tool for predefined factual questions and falls back to a powerful LLM (Groq Llama 3.1) for everything else.
- **Agentic Routing**: A simple agent graph intelligently routes user queries to the appropriate tool (local search or LLM) based on a heuristic analysis of the query.
- **Stateful Conversations**: Maintains a conversation history for each user to provide contextual responses.
- **FastAPI Service**: Exposes the agent's functionality through a clean, easy-to-use REST API.
- **LangGraph Demonstrations**: Includes Jupyter notebooks that showcase how to build similar agentic systems using `langgraph`.

## How It Works

The core logic resides in the `AgentGraph` class (`graph.py`). When a query is received:

1.  **Factual Check**: The system first uses the `is_factual()` function to determine if the query is likely a factual question (e.g., starts with "What is...", "Who is...", etc.).
2.  **Tool Search**: If the query is deemed factual, the `small_search_tool()` is invoked. This tool performs a fuzzy search against a predefined set of questions and answers stored in `data/facts.json`. If a confident match is found, the answer is returned immediately with `"source": "tool"`.
3.  **LLM Fallback**: If the query is not factual or the local tool finds no answer, the query (along with recent conversation history) is passed to a Groq Llama 3.1 model via the `answer_question()` function. The LLM generates a response, which is returned with `"source": "llm"`.
4.  **Memory Management**: Each user interaction (user query and assistant response) is stored in a `Memory` object, which is a `deque` with a fixed length to maintain recent context.

## Setup and Installation

### Prerequisites

- Python 3.7+
- A Groq API Key

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/tg1106/question-answer-agentic-ai.git
    cd question-answer-agentic-ai
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a file named `.env` in the root of the project and add your Groq API key:
    ```
    GROQ_API_KEY="your_groq_api_key_here"
    ```

## Running the Application

To start the FastAPI server, run the following command from the project root:

```bash
uvicorn main:app --reload
```

The server will be available at `http://localhost:8000`.

## API Usage

You can interact with the agent using any HTTP client, such as `curl` or `requests`.

### `/chat`

Send a message to the agent and get a response.

-   **Method**: `POST`
-   **Body**:
    ```json
    {
      "message": "Your question here",
      "user_id": "user123"
    }
    ```
-   **Example with `curl`:**

    *Factual query (handled by the tool):*
    ```bash
    curl -X POST "http://localhost:8000/chat" \
    -H "Content-Type: application/json" \
    -d '{"message": "What is FastAPI?", "user_id": "user123"}'
    ```
    *Response:*
    ```json
    {
      "answer": "(tool) FastAPI is a high-performance Python web framework for building APIs.",
      "source": "tool",
      "memory": [
        { "role": "user", "text": "What is FastAPI?" },
        { "role": "assistant", "text": "(tool) FastAPI is a high-performance Python web framework for building APIs." }
      ]
    }
    ```

    *Conversational query (handled by the LLM):*
    ```bash
    curl -X POST "http://localhost:8000/chat" \
    -H "Content-Type: application/json" \
    -d '{"message": "Tell me a short joke.", "user_id": "user123"}'
    ```

### `/clear_memory`

Clear the conversation history for a specific user.

-   **Method**: `POST`
-   **Query Parameter**: `user_id` (string)
-   **Example with `curl`:**
    ```bash
    curl -X POST "http://localhost:8000/clear_memory?user_id=user123"
    ```
    *Response:*
    ```json
    {
      "status": "cleared",
      "user_id": "user123"
    }
    ```

## Project Structure

```
├── README.md
├── graph.py            # Defines the core AgentGraph for routing queries.
├── main.py             # FastAPI application entry point.
├── requirements.txt
├── agents/
│   ├── fact_detection.py # Logic for identifying factual queries and the local search tool.
│   ├── interface.py      # Interface to the Groq LLM.
│   └── memory.py         # Manages conversation history.
├── chatbot/              # Jupyter notebooks for demonstration and testing.
│   ├── bot.ipynb
│   ├── customerbot.ipynb
│   └── toolbot.ipynb
└── data/
    └── facts.json        # The local knowledge base for the search tool.
