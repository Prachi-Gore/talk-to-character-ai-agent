from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from app.prompts import quiz_chain, evaluation_chain
from app.vector_store import get_relevant_summary
from typing import TypedDict, List

class QuizState(TypedDict):
    book_id: str
    quiz: str
    user_answers: List[str]
    evaluation: str

# --- Nodes ---
class QuizNode:
    def run(self, state: dict):
        # Get book summary
        book_id = state.get("book_id")
        if not book_id:
            raise ValueError("book_id is missing in state")

        summary = get_relevant_summary(book_id)

        # Run the quiz generation pipeline
        quiz = quiz_chain.invoke({"context": summary})

        return {"quiz": quiz}


class EvaluationNode:
    def run(self, state: dict):
        questions = state.get("quiz")
        user_answers = state.get("user_answers")

        if not questions or not user_answers:
            raise ValueError("Quiz questions or user answers missing in state.")

        eval_result = evaluation_chain.invoke({
            "questions": questions,
            "user_answers": user_answers
        })

        return {"evaluation": eval_result}

def create_quiz_graph():
    # Create a workflow graph for the quiz
    workflow = StateGraph(QuizState)

    # Add nodes with the updated run methods
    workflow.add_node("QuizNode", QuizNode().run)
    workflow.add_node("EvaluationNode", EvaluationNode().run)

    # Define the flow between nodes
    workflow.add_edge("QuizNode", "EvaluationNode")

    # Set entry and exit points
    workflow.set_entry_point("QuizNode")
    workflow.set_finish_point("EvaluationNode")

    # Compile the graph to make it executable
    compiled_workflow = workflow.compile()

    return compiled_workflow