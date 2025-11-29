# agents/memory.py
from collections import deque
from typing import List, Dict, Optional


DEFAULT_MAXLEN = 6  


class Memory:
    def __init__(self, maxlen: int = DEFAULT_MAXLEN):
        self.maxlen = int(maxlen)
        self._dq = deque(maxlen=self.maxlen)

    def append(self, role: str, text: str) -> None:
        if not isinstance(role, str) or not isinstance(text, str):
            raise ValueError("role and text must be strings")
        self._dq.append({"role": role, "text": text})

    def to_list(self) -> List[Dict[str, str]]:
        return list(self._dq)

    def get_recent(self, n: Optional[int] = None) -> List[Dict[str, str]]:
        if n is None:
            return list(self._dq)
        n = max(0, int(n))
        return list(self._dq)[-n:] if n > 0 else []

    def clear(self) -> None:
        self._dq.clear()

    def load(self, items: List[Dict[str, str]]):
        if not isinstance(items, list):
            raise ValueError("load expects a list of dicts")
        self.clear()
        for item in items[-self.maxlen:]:
            role = item.get("role")
            text = item.get("text")
            if role and text:
                self.append(role, text)
