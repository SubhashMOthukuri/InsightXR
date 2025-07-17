#!/usr/bin/env python3
"""
Check what's stored in Chroma database
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

def main():
    print("🔍 Checking Chroma database contents...")
    
    # Setup embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Load existing Chroma database
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    
    # Get collection info
    collection = vectorstore._collection
    count = collection.count()
    
    print(f"📊 Total documents in Chroma: {count}")
    
    if count > 0:
        print("\n📄 Sample documents:")
        # Get all documents
        results = collection.get()
        
        if results['documents']:
            for i, (doc, metadata) in enumerate(zip(results['documents'][:5], results['metadatas'][:5])):
                print(f"\n--- Document {i+1} ---")
                print(f"Content preview: {doc[:200]}...")
                print(f"Metadata: {metadata}")
    else:
        print("❌ No documents found in Chroma database!")
        print("💡 You need to ingest your documents first.")
        print("   Run: python src/ingest.py")

if __name__ == "__main__":
    main() 