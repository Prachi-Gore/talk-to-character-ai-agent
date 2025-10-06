from fastapi import FastAPI
from app.models import BookSchema, QuizRequest, EvaluateRequest
from app.vector_store import add_book_to_vector_db,get_relevant_summary
from app.quiz_graph import evaluate_quiz_graph
from app.prompts import quiz_chain
from langchain_core.output_parsers.json import JsonOutputParser
import json

json_parser = JsonOutputParser()

app = FastAPI(title="Book Quiz AI Agent")

graph = evaluate_quiz_graph()

@app.post("/add_book_summary")
async def add_book(book: BookSchema):
   await add_book_to_vector_db(book.id, book.title, book.author)
    # return {"message": "Book added successfully"}

@app.post("/generate_quiz")
async def generate_quiz(req: QuizRequest):
     # Get book summary
    book_id = req.get("book_id")
    if not book_id:
        raise ValueError("book_id is missing in state")

    summary = get_relevant_summary(book_id)
    ai_generated_quiz = await quiz_chain.ainvoke({"context": summary})
    quiz_array=json_parser.parse(ai_generated_quiz)
    return {"quiz": quiz_array}

@app.post("/evaluate_answers")
async def evaluate_answers(req: EvaluateRequest):
    quiz_details=json.dumps(req.quiz) # convert list of dicts to JSON string
    state = {"book_id": req.book_id, "quiz": quiz_details, "user_answers": req.user_answers, "evaluation": ""}
    result =await graph.ainvoke(state)
    return {"evaluation": result["evaluation"]}
