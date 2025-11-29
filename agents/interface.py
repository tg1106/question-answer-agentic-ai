# agents/interface.py
import os
from typing import List, Dict

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment. Set it before running the app.")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant"    
)

prompt_template = ChatPromptTemplate.from_template("""
You are a helpful and concise Question-Answer assistant.

Conversation memory (most recent last):
{memory}

User: {query}
Assistant:
""")


def format_memory(memory: List[Dict[str, str]]) -> str:
    if not memory:
        return "(no previous messages)"

    lines = []
    for item in memory:
        role = item.get("role", "?")
        text = item.get("text", "")
        lines.append(f"{role}: {text}")
    return "\n".join(lines)


def answer_question(query: str, memory: List[Dict[str, str]]) -> str:
    mem_text = format_memory(memory)

    try:
        # Modern LangChain format()
        messages = prompt_template.format_messages(
            memory=mem_text,
            query=query
        )

        response = llm.invoke(messages)
        return response.content.strip()

    except Exception as e:
        return f"LLM error: {str(e)}"

