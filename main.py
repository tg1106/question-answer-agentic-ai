from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from collections import defaultdict

from agents.memory import Memory
from agents.fact_detection import small_search_tool, is_factual
from agents.interface import answer_question
from graph import build_agent_graph

app = FastAPI(title="Question-Answer Agentic AI")

USER_MEMORY: Dict[str, Memory] = defaultdict(lambda: Memory(maxlen=6))

agent_graph = build_agent_graph(memory_maxlen=6)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "anon"


class ChatResponse(BaseModel):
    answer: str
    source: str
    memory: list

def get_user_memory(user_id: str) -> Memory:
    return USER_MEMORY[user_id]

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    user_id = req.user_id or "anon"
    memory = get_user_memory(user_id)

    memory.append("user", req.message)

    result = agent_graph.route_query(req.message, memory)

    answer = result["answer"]
    source = result["source"]

    memory.append("assistant", answer)

    return ChatResponse(
        answer=answer,
        source=source,
        memory=memory.to_list()
    )


@app.post("/clear_memory")
def clear_memory(user_id: str = "anon"):
    memory = get_user_memory(user_id)
    memory.clear()
    return {"status": "cleared", "user_id": user_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
