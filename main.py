from fastapi import FastAPI
from app.models import BookSchema, QuizRequest, EvaluateRequest
from app.vector_store import add_book_to_vector_db
from app.quiz_graph import create_quiz_graph

app = FastAPI(title="Book Quiz AI Agent")

graph = create_quiz_graph()

@app.post("/add_book_summary")
def add_book(book: BookSchema):
    add_book_to_vector_db(book.id, book.title, book.author)
    # return {"message": "Book added successfully"}

@app.post("/generate_quiz")
def generate_quiz(req: QuizRequest):
    state = {"book_id": req.book_id, "quiz": "", "user_answers": [], "evaluation": ""}
    result = graph.invoke(state)
    return {"quiz": result["quiz"]}

@app.post("/evaluate_answers")
def evaluate_answers(req: EvaluateRequest):
    state = {"book_id": req.book_id, "quiz": "", "user_answers": req.user_answers, "evaluation": ""}
    result = graph.invoke(state)
    return {"evaluation": result["evaluation"]}
