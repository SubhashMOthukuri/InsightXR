#!/usr/bin/env python3
"""
Setup script for Pinecone index
"""
import os
from dotenv import load_dotenv
import pinecone

load_dotenv()

# Get environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY environment variable is not set.")
if not PINECONE_ENVIRONMENT:
    raise ValueError("PINECONE_ENVIRONMENT environment variable is not set.")

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

INDEX_NAME = "aidocrag"
DIMENSION = 384  # For all-MiniLM-L6-v2 model

def main():
    print(f"Checking Pinecone indexes in environment: {PINECONE_ENVIRONMENT}")
    
    # List all indexes
    try:
        indexes = pinecone.list_indexes()
        print(f"Found {len(indexes)} indexes:")
        for index in indexes:
            print(f"  - {index}")
    except Exception as e:
        print(f"Error listing indexes: {e}")
        return
    
    # Check if our index exists
    if INDEX_NAME in indexes:
        print(f"✅ Index '{INDEX_NAME}' already exists!")
        return
    
    # Create the index
    print(f"Creating index '{INDEX_NAME}'...")
    try:
        pinecone.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric="cosine"
        )
        print(f"✅ Successfully created index '{INDEX_NAME}'!")
        print(f"   Dimension: {DIMENSION}")
        print(f"   Metric: cosine")
    except Exception as e:
        print(f"❌ Error creating index: {e}")

if __name__ == "__main__":
    main() 