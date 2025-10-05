from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(
    model="gpt-3.5-turbo",  # cheaper model suitable for free trial
    temperature=0.6, # creativeness moderate
    api_key=os.getenv("OPENAI_API_KEY"),
)
# --- Quiz Generator ---
quiz_prompt = ChatPromptTemplate.from_template("""
You are a quiz master.
Generate 5 thought-provoking multiple-choice questions (MCQs)
from the following book summary.

Book Summary:
{context}

Return them in JSON format:
[
  {"question": "...", "options": ["A", "B", "C", "D"], "correct": "A"},
  ...
]
""")

quiz_chain = quiz_prompt | llm

# --- Answer Evaluator ---
evaluation_prompt = ChatPromptTemplate.from_template("""
You are an evaluator.
Evaluate user's answers based on these quiz questions and correct answers.

Questions:
{questions}

User Answers:
{user_answers}

Give score out of 5 and a feedback summary (pros & cons).
Return response as:
{{"score": int, "feedback": "string"}}
""")

evaluation_chain = evaluation_prompt | llm

summary_prompt = ChatPromptTemplate.from_template(
    "Write a 100 lines of summary for the book '{title}' by {author}."
)
summary_chain = summary_prompt | llm

