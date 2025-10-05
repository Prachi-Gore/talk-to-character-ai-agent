# Memory / checkpoint management

from typing import Dict, List

memory_store: Dict[str, List[Dict]] = {}

def save_quiz_history(user_id: str, book_id: str, question: str, answer: str, score: int):
    key = f"{user_id}_{book_id}"
    if key not in memory_store:
        memory_store[key] = []
    memory_store[key].append({"question": question, "answer": answer, "score": score})

def get_quiz_history(user_id: str, book_id: str):
    key = f"{user_id}_{book_id}"
    return memory_store.get(key, [])
