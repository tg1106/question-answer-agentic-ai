from typing import Optional, Dict
from pathlib import Path
import json
import difflib
import re

DEFAULT_FACTS_PATH = str(Path(__file__).resolve().parents[1] / "data" / "facts.json")

# load facts once at import time
def load_facts(path: str = DEFAULT_FACTS_PATH) -> Dict[str, str]:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        with p.open('r', encoding='utf-8') as f:
            data = json.load(f)
        return {k.lower().strip(): v for k, v in data.items()}
    except Exception:
        return {}

_FACTS = load_facts()

def small_search_tool(query: str) -> Optional[str]:
    if not query or not isinstance(query, str):
        return None
    q = query.lower().strip()
    if q in _FACTS:
        return _FACTS[q]
    q_clean = re.sub(r'[^a-z0-9\s]', '', q).strip()
    if q_clean in _FACTS:
        return _FACTS[q_clean]
    keys = list(_FACTS.keys())
    matches = difflib.get_close_matches(q_clean, keys, n=1, cutoff=0.6)
    if matches:
        return _FACTS.get(matches[0])
    return None


def is_factual(query: str) -> bool:
    
    if not query or not isinstance(query, str):
        return False
    q = query.strip().lower()
    question_words = ['what', 'who', 'when', 'where', 'which', 'how', 'why']
    if any(q.startswith(w + ' ') or q.startswith(w + '?') or q == w for w in question_words):
        return True
    if '?' in q:
        return True
    if re.search(r'\b\d{1,4}\b', q) or re.search(r'\d+%|\$|₹|£|€', q):
        return True
    factual_keywords = ['define', 'definition', 'meaning', 'price', 'cost', 'population', 'capital', 'president', 'prime minister']
    if any(kw in q for kw in factual_keywords):
        return True
    return False
