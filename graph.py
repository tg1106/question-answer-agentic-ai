# graph.py

from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass

from agents.fact_detection import is_factual, small_search_tool
from agents.interface import answer_question  
from agents.memory import Memory


@dataclass
class AgentResult:
    answer: str
    source: str  
    metadata: Optional[Dict[str, Any]] = None


class AgentGraph:
    def __init__(self, *, memory_maxlen: int = 6) -> None:
        self.memory_maxlen = int(memory_maxlen)

    def _ensure_memory_list(self, memory: Union[Memory, List[Dict[str, str]], None]) -> List[Dict[str, str]]:
        if memory is None:
            return []
        if isinstance(memory, Memory):
            return memory.to_list()
        if isinstance(memory, list):
            return memory
        try:
            return list(memory)
        except Exception:
            return []

    def route_query(self, query: str, memory: Union[Memory, List[Dict[str, str]], None] = None) -> Dict[str, Any]:
        if not isinstance(query, str) or not query.strip():
            return {"answer": "Invalid or empty query.", "source": "error", "metadata": {"reason": "empty_query"}}

        mem_list = self._ensure_memory_list(memory)

        try:
            factual = is_factual(query)
        except Exception:
            factual = False  

        if factual:
            try:
                tool_ans = small_search_tool(query)
            except Exception:
                tool_ans = None

            if tool_ans:
                return {"answer": f"(tool) {tool_ans}", "source": "tool", "metadata": {"tool_match": True}}
            
        try:
            llm_response = answer_question(query, mem_list)
        except Exception as e:
            return {
                "answer": f"LLM error: {str(e)}",
                "source": "error",
                "metadata": {"error_type": type(e).__name__}
            }

        return {"answer": llm_response, "source": "llm", "metadata": {"tool_match": False}}

def build_agent_graph(*, memory_maxlen: int = 6) -> AgentGraph:

    return AgentGraph(memory_maxlen=memory_maxlen)


if __name__ == "__main__":
    g = build_agent_graph()
    print(g.route_query("What is Python?", memory=[]))  
    print(g.route_query("Tell me a joke.", memory=[]))   
