# Build LangChain RAG
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from pydantic import SecretStr
from utils.logger import setup_logger

load_dotenv()
print("PINECONE_ENVIRONMENT:", os.getenv("PINECONE_ENVIRONMENT"))
print("PINECONE_API_KEY:", os.getenv("PINECONE_API_KEY"))
logger = setup_logger(__name__)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY environment variable is not set.")
if not PINECONE_ENVIRONMENT:
    raise ValueError("PINECONE_ENVIRONMENT environment variable is not set.")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Setup embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Setup Chroma vector store (local)
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Setup OpenAI chat model
llm = ChatOpenAI(api_key=SecretStr(OPENAI_API_KEY), model="gpt-4", temperature=0)

# Build the RAG QA chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # "stuff" concatenates docs; for longer context try "map_reduce" or "refine"
    retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4}),
    return_source_documents=True
)

def answer_query(query):
    logger.info(f"Received query: {query}")
    result = rag_chain({"query": query})
    logger.info("Answer generated.")
    return {
        "answer": result["result"],
        "source_docs": result["source_documents"]
    }
