# Load, chunk, embed, and store in Chroma
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from utils.logger import setup_logger
from ocr_utils import process_documents_folder

load_dotenv()
logger = setup_logger(__name__)

# Setup embeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Setup Chroma vector store
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Setup text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
)

def ingest_documents(folder_path):
    documents = process_documents_folder(folder_path)
    logger.info(f"Processing {len(documents)} documents...")

    all_chunks = []
    
    for doc in documents:
        logger.info(f"Processing document: {doc['filename']}")
        
        # Create LangChain Document
        langchain_doc = Document(
            page_content=doc["text"],
            metadata={
                "document_id": doc["document_id"],
                "filename": doc["filename"],
                "timestamp": doc["timestamp"]
            }
        )
        
        # Split into chunks
        chunks = text_splitter.split_documents([langchain_doc])
        logger.info(f"Chunked document '{doc['filename']}' into {len(chunks)} chunks.")
        
        all_chunks.extend(chunks)

    # Add all chunks to Chroma
    if all_chunks:
        vectorstore.add_documents(all_chunks)
        logger.info(f"Added {len(all_chunks)} chunks to Chroma database.")
    else:
        logger.warning("No chunks to add to database.")

    logger.info("Ingestion completed.")

if __name__ == "__main__":
    ingest_documents("./data")
