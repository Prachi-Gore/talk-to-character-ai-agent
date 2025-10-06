from pydantic import BaseModel
from typing import List

class BookSchema(BaseModel):
    id: str
    title: str
    author: str

class QuizRequest(BaseModel):
    book_id: str

class EvaluateRequest(BaseModel):
    book_id: str
    user_answers: List[str]
    questions:List[str]
