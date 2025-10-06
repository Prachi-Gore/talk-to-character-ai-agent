from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from app.prompts import summary_chain

# Load environment variables from .env
load_dotenv() 
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
print("OPENAI_KEY ",OPENAI_KEY)
PERSIST_DIR = "vector_db/chroma_db"
os.makedirs(PERSIST_DIR, exist_ok=True)
embedding = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma(
    collection_name="book_summaries",
    embedding_function=embedding,
    persist_directory=PERSIST_DIR
)

async def add_book_to_vector_db(book_id: str, title: str, author: str):
    summary = await summary_chain.ainvoke({
        "title": title,
        "author": author
    })

    """Store book summary embeddings in Chroma"""
    vectorstore.add_texts(
        texts=[summary],
        metadatas=[{"book_id": book_id, "title": title, "author": author}]
    )
    vectorstore.persist()

def get_relevant_summary(book_id: str):
    """Retrieve relevant summary for RAG"""
    docs = vectorstore.similarity_search(book_id, k=1)
    return docs[0].page_content if docs else ""
